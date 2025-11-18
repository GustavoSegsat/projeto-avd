from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
from minio import Minio
from minio.error import S3Error
import io
import os
from datetime import datetime
import psycopg2
from psycopg2.extras import execute_values
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="INMET Data Ingestion API", version="1.0.0")

# Configurações
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "minio:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
MINIO_BUCKET = os.getenv("MINIO_BUCKET", "inmet-data")

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "inmet_db")

# Cliente MinIO
minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

def get_db_connection():
    return psycopg2.connect(
        host=POSTGRES_HOST,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        database=POSTGRES_DB
    )

def ensure_bucket_exists():
    """Garante que o bucket existe no MinIO"""
    try:
        if not minio_client.bucket_exists(MINIO_BUCKET):
            minio_client.make_bucket(MINIO_BUCKET)
            logger.info(f"Bucket {MINIO_BUCKET} criado com sucesso")
    except S3Error as e:
        logger.error(f"Erro ao criar bucket: {e}")
        raise

def parse_inmet_csv(content: bytes) -> pd.DataFrame:
    """Parse do CSV do INMET, pulando cabeçalho e tratando encoding"""
    try:
        # Lê o arquivo pulando as primeiras 8 linhas (cabeçalho da estação)
        df = pd.read_csv(
            io.BytesIO(content),
            skiprows=8,
            sep=';',
            encoding='latin-1',
            decimal=',',
            na_values=['', ' ', 'NaN', 'N/A']
        )
        
        # Renomeia colunas para facilitar
        column_mapping = {
            'Data': 'data',
            'Hora UTC': 'hora_utc',
            'PRECIPITAÇÃO TOTAL, HORÁRIO (mm)': 'precipitacao',
            'PRESSAO ATMOSFERICA AO NIVEL DA ESTACAO, HORARIA (mB)': 'pressao',
            'RADIACAO GLOBAL (Kj/m²)': 'radiacao',
            'TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)': 'temperatura',
            'UMIDADE RELATIVA DO AR, HORARIA (%)': 'umidade',
            'VENTO, DIREÇÃO HORARIA (gr) (° (gr))': 'vento_direcao',
            'VENTO, VELOCIDADE HORARIA (m/s)': 'vento_velocidade'
        }
        
        df = df.rename(columns=column_mapping)
        
        # Seleciona apenas as colunas necessárias
        required_cols = ['data', 'hora_utc', 'precipitacao', 'pressao', 
                        'radiacao', 'temperatura', 'umidade', 
                        'vento_direcao', 'vento_velocidade']
        
        df = df[[col for col in required_cols if col in df.columns]]
        
        # Converte data e hora
        df['data'] = pd.to_datetime(df['data'], format='%Y/%m/%d', errors='coerce')
        df['hora_utc'] = df['hora_utc'].str.replace(' UTC', '').str.zfill(4)
        df['datetime'] = pd.to_datetime(
            df['data'].astype(str) + ' ' + df['hora_utc'],
            format='%Y-%m-%d %H%M',
            errors='coerce'
        )
        
        # Remove linhas com datetime inválido
        df = df.dropna(subset=['datetime'])
        
        # Converte colunas numéricas
        numeric_cols = ['precipitacao', 'pressao', 'radiacao', 'temperatura', 
                       'umidade', 'vento_direcao', 'vento_velocidade']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Remove duplicatas
        df = df.drop_duplicates(subset=['datetime'])
        df = df.sort_values('datetime')
        
        return df
    except Exception as e:
        logger.error(f"Erro ao processar CSV: {e}")
        raise

def save_to_minio(df: pd.DataFrame, filename: str):
    """Salva DataFrame como CSV no MinIO"""
    ensure_bucket_exists()
    
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_bytes = csv_buffer.getvalue().encode('utf-8')
    
    object_name = f"raw/{filename}"
    minio_client.put_object(
        MINIO_BUCKET,
        object_name,
        io.BytesIO(csv_bytes),
        length=len(csv_bytes),
        content_type='text/csv'
    )
    logger.info(f"Dados salvos no MinIO: {object_name}")
    return object_name

def save_to_postgres(df: pd.DataFrame):
    """Salva DataFrame no PostgreSQL"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Cria tabela se não existir
        create_table_query = """
        CREATE TABLE IF NOT EXISTS dados_meteorologicos (
            id SERIAL PRIMARY KEY,
            datetime TIMESTAMP UNIQUE NOT NULL,
            data DATE,
            hora_utc VARCHAR(10),
            precipitacao FLOAT,
            pressao FLOAT,
            radiacao FLOAT,
            temperatura FLOAT,
            umidade FLOAT,
            vento_direcao FLOAT,
            vento_velocidade FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        
        # Prepara dados para inserção
        df_insert = df.copy()
        df_insert['data'] = df_insert['datetime'].dt.date
        
        columns = ['datetime', 'data', 'hora_utc', 'precipitacao', 'pressao', 
                  'radiacao', 'temperatura', 'umidade', 'vento_direcao', 'vento_velocidade']
        
        values = [tuple(row) for row in df_insert[columns].values]
        
        insert_query = """
        INSERT INTO dados_meteorologicos 
        (datetime, data, hora_utc, precipitacao, pressao, radiacao, 
         temperatura, umidade, vento_direcao, vento_velocidade)
        VALUES %s
        ON CONFLICT (datetime) DO UPDATE SET
            precipitacao = EXCLUDED.precipitacao,
            pressao = EXCLUDED.pressao,
            radiacao = EXCLUDED.radiacao,
            temperatura = EXCLUDED.temperatura,
            umidade = EXCLUDED.umidade,
            vento_direcao = EXCLUDED.vento_direcao,
            vento_velocidade = EXCLUDED.vento_velocidade
        """
        
        execute_values(cursor, insert_query, values)
        conn.commit()
        logger.info(f"{len(values)} registros inseridos/atualizados no PostgreSQL")
        
    except Exception as e:
        conn.rollback()
        logger.error(f"Erro ao salvar no PostgreSQL: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

@app.on_event("startup")
async def startup_event():
    """Inicializa serviços na startup"""
    ensure_bucket_exists()
    logger.info("FastAPI iniciado e pronto para receber dados")

@app.get("/")
async def root():
    return {
        "message": "INMET Data Ingestion API",
        "version": "1.0.0",
        "endpoints": {
            "upload": "/upload",
            "health": "/health"
        }
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "fastapi"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Endpoint para upload de arquivo CSV do INMET"""
    try:
        # Lê o arquivo
        content = await file.read()
        
        # Processa CSV
        df = parse_inmet_csv(content)
        
        if df.empty:
            raise HTTPException(status_code=400, detail="CSV vazio ou inválido")
        
        # Gera nome do arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{file.filename}_{timestamp}.csv"
        
        # Salva no MinIO
        object_name = save_to_minio(df, filename)
        
        # Salva no PostgreSQL
        save_to_postgres(df)
        
        return JSONResponse({
            "message": "Arquivo processado com sucesso",
            "filename": filename,
            "object_name": object_name,
            "records": len(df),
            "date_range": {
                "start": df['datetime'].min().isoformat(),
                "end": df['datetime'].max().isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"Erro no upload: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
async def get_stats():
    """Retorna estatísticas dos dados armazenados"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                COUNT(*) as total_records,
                MIN(datetime) as min_date,
                MAX(datetime) as max_date,
                AVG(temperatura) as avg_temp,
                AVG(umidade) as avg_umidade,
                AVG(pressao) as avg_pressao
            FROM dados_meteorologicos
        """)
        
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        return {
            "total_records": result[0],
            "date_range": {
                "min": result[1].isoformat() if result[1] else None,
                "max": result[2].isoformat() if result[2] else None
            },
            "averages": {
                "temperatura": round(result[3], 2) if result[3] else None,
                "umidade": round(result[4], 2) if result[4] else None,
                "pressao": round(result[5], 2) if result[5] else None
            }
        }
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas: {e}")
        raise HTTPException(status_code=500, detail=str(e))


