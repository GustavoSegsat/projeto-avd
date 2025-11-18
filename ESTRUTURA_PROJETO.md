# 📁 Estrutura do Projeto

```
Projeto AVD/
│
├── docker-compose.yml          # Orquestração de todos os serviços
│
├── fastapi/                    # API de Ingestão
│   ├── Dockerfile
│   ├── main.py                 # Código principal da API
│   └── requirements.txt        # Dependências Python
│
├── jupyterlab/                 # Ambiente de Análise
│   ├── Dockerfile
│   └── jupyter_lab_config.py   # Configuração do Jupyter
│
├── mlflow/                     # Versionamento de Modelos
│   ├── Dockerfile
│   └── init_minio.sh           # Script de inicialização
│
├── notebooks/                  # Notebooks de Análise
│   ├── 01_tratamento_dados.ipynb
│   ├── 02_modelagem_temperatura.ipynb
│   └── 03_visualizacoes.ipynb
│
├── sql_scripts/                # Scripts SQL
│   ├── 01_create_tables.sql    # Tabelas principais
│   └── 02_create_thingsboard_db.sql
│
├── reports/                    # Relatórios
│   └── relatorio_tecnico.md    # Template do relatório
│
├── data/                       # Dados locais (volume Docker)
├── trendz/                     # Dashboards exportados
│
├── README.md                   # Documentação principal
├── QUICKSTART.md               # Guia rápido
├── LICENSE                     # Licença MIT
├── upload_data.py              # Script auxiliar de upload
└── INMET_NE_PE_A301_RECIFE_01-01-2021_A_31-12-2021.CSV  # Dataset
```

## 🔄 Fluxo de Dados

```
CSV → FastAPI → MinIO (raw) + PostgreSQL (structured)
                    ↓
            JupyterLab (tratamento)
                    ↓
            JupyterLab (modelagem)
                    ↓
            MLFlow (versionamento)
                    ↓
            ThingsBoard (visualização)
```

## 🛠️ Tecnologias por Camada

### Ingestão
- **FastAPI**: Framework web moderno e rápido
- **MinIO**: Armazenamento S3-compatible
- **PostgreSQL**: Banco de dados relacional

### Processamento
- **JupyterLab**: Ambiente interativo de análise
- **pandas**: Manipulação de dados
- **scikit-learn**: Machine Learning

### Versionamento
- **MLFlow**: Tracking de experimentos
- **PostgreSQL**: Backend store do MLFlow
- **MinIO**: Artifact store do MLFlow

### Visualização
- **ThingsBoard**: Plataforma IoT para dashboards
- **matplotlib/seaborn**: Gráficos estáticos
- **plotly**: Gráficos interativos

## 📊 Dados Processados

### Tabelas no PostgreSQL

1. **dados_meteorologicos**: Dados brutos ingeridos
   - datetime, temperatura, umidade, pressao, etc.

2. **dados_tratados**: Dados após limpeza e feature engineering
   - Inclui features temporais e cíclicas

3. **predicoes_temperatura**: Resultados das predições
   - temperatura_real, temperatura_predita, rmse

### Buckets no MinIO

1. **inmet-data/raw/**: Dados brutos em CSV
2. **mlflow-artifacts/**: Modelos versionados pelo MLFlow

## 🎯 Objetivo do Projeto

Prever a **temperatura horária** usando:
- Variáveis meteorológicas (umidade, pressão, radiação, vento, precipitação)
- Features temporais (hora, mês, dia do ano)
- Features cíclicas (seno/cosseno de hora e mês)

## 📈 Modelos Implementados

1. **Random Forest Regressor**
2. **Gradient Boosting Regressor**

Métricas: RMSE, MAE, R²


