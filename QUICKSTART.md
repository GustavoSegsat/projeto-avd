# 🚀 Guia Rápido de Inicialização

## Passo a Passo para Executar o Pipeline

### 1. Iniciar os Serviços

```bash
docker-compose up -d
```

Aguarde 2-3 minutos para todos os serviços iniciarem. Verifique o status:

```bash
docker-compose ps
```

### 2. Verificar Logs (Opcional)

```bash
# Ver logs de todos os serviços
docker-compose logs -f

# Ver logs de um serviço específico
docker-compose logs -f fastapi
```

### 3. Fazer Upload do CSV

**Opção 1: Usando o script Python**
```bash
python upload_data.py
```

**Opção 2: Usando curl (PowerShell)**
```powershell
curl -X POST "http://localhost:8000/upload" -F "file=@INMET_NE_PE_A301_RECIFE_01-01-2021_A_31-12-2021.CSV"
```

**Opção 3: Usando a interface web**
Acesse http://localhost:8000/docs e use o endpoint `/upload`

### 4. Verificar Dados Inseridos

```bash
# Ver estatísticas via API
curl http://localhost:8000/stats
```

### 5. Executar Análises no JupyterLab

1. Acesse http://localhost:8888
2. Abra o notebook `01_tratamento_dados.ipynb`
3. Execute todas as células (Cell > Run All)
4. Repita para `02_modelagem_temperatura.ipynb`
5. Por fim, execute `03_visualizacoes.ipynb`

### 6. Acessar MLFlow

1. Acesse http://localhost:5000
2. Veja os experimentos e modelos treinados
3. Compare métricas dos diferentes modelos

### 7. Configurar ThingsBoard (Opcional)

1. Acesse http://localhost:8080
2. Login padrão:
   - Email: `tenant@thingsboard.org`
   - Senha: `tenant`
3. Configure dashboards conforme necessário

## 🔍 Verificações de Saúde

### Testar FastAPI
```bash
curl http://localhost:8000/health
```

### Testar PostgreSQL
```bash
docker exec -it postgres psql -U postgres -d inmet_db -c "SELECT COUNT(*) FROM dados_meteorologicos;"
```

### Testar MinIO
Acesse http://localhost:9001 (usuário: `minioadmin`, senha: `minioadmin`)

## ⚠️ Problemas Comuns

### Serviços não iniciam
```bash
# Pare todos os serviços
docker-compose down

# Remova volumes (CUIDADO: apaga dados)
docker-compose down -v

# Reconstrua as imagens
docker-compose build --no-cache

# Inicie novamente
docker-compose up -d
```

### Erro de conexão com banco
Aguarde mais alguns segundos. O PostgreSQL pode levar tempo para inicializar.

### Porta já em uso
Verifique se alguma aplicação está usando as portas:
- 8000 (FastAPI)
- 5432 (PostgreSQL)
- 8888 (JupyterLab)
- 5000 (MLFlow)
- 8080 (ThingsBoard)
- 9000/9001 (MinIO)

## 📊 Próximos Passos

Após executar os notebooks:
1. Analise os gráficos gerados
2. Compare modelos no MLFlow
3. Exporte visualizações para o relatório
4. Configure dashboards no ThingsBoard


