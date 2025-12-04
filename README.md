# Pipeline de Análise e Visualização de Dados Meteorológicos - INMET

## 📋 Informações do Projeto

**Disciplina:** Análise e Visualização de Dados - 2025.2  
**Instituição:** CESAR School  
**Problema:** Previsão de Temperatura Horária com base em variáveis meteorológicas

## 👥 Membros do Projeto

| Nome              | GitHub |
|-------------------|--------|
| Gustavo Carneiro  | [@GustavoSegsat](https://github.com/GustavoSegsat) |
| João Marcelo      | [@a-guy-and-his-computer](https://github.com/a-guy-and-his-computer) |
| Thiago Queiroz    | [@tempzz7](https://github.com/tempzz7) |
| Matheus Araujo    | [@MathhAraujo](https://github.com/MathhAraujo) |
| Felipe Santos     | [@Felipesmarq](https://github.com/Felipesmarq) |
| Felipe Queiroz    | [@Felipebq1](https://github.com/Felipebq1) |
| Pedro Antônio     | [@lovepxdro](https://github.com/lovepxdro) |
| Júlia Sales       | [@julsales](https://github.com/julsales) |


## 🎯 Objetivo

Desenvolver um pipeline completo de análise e visualização que integre:
- Coleta de dados meteorológicos do INMET (CSV)
- Armazenamento estruturado em PostgreSQL e MinIO
- Tratamento e limpeza de dados
- Modelagem preditiva (regressão para previsão de temperatura horária)
- Visualização interativa via ThingsBoard

## 🏗️ Arquitetura

O pipeline é composto pelos seguintes serviços:

| Serviço | Porta | Função |
|---------|-------|--------|
| FastAPI | 8000 | API de ingestão de dados |
| MinIO | 9000/9001 | Armazenamento de objetos (S3-compatible) |
| PostgreSQL | 5432 | Banco de dados estruturado |
| JupyterLab | 8888 | Ambiente de análise e modelagem |
| MLFlow | 5000 | Versionamento de modelos |
| ThingsBoard | 8080 | Dashboard e visualização |

## 🚀 Instalação e Execução

### Pré-requisitos

- Docker Desktop instalado e rodando
- Docker Compose v2.0+
- 8GB+ de RAM disponível

### Passos para Execução

1. **Clone o repositório:**
```bash
git clone <url-do-repositorio>
cd "Projeto AVD"
```

2. **Inicie os serviços:**
```bash
docker-compose up -d
```

3. **Aguarde os serviços iniciarem (pode levar 2-3 minutos):**
```bash
docker-compose ps
```

4. **Faça upload do arquivo CSV via API:**
```bash
# Windows PowerShell
curl -X POST "http://localhost:8000/upload" -F "file=@INMET_SE_RJ_A652_RIO DE JANEIRO - FORTE DE COPACABANA_01-01-2024_A_31-12-2024.CSV"

# Ou usando o script Python
python upload_data.py "fastapi/INMET_SE_RJ_A652_RIO DE JANEIRO - FORTE DE COPACABANA_01-01-2024_A_31-12-2024.CSV"

# Ou usando Python diretamente
python -c "import requests; requests.post('http://localhost:8000/upload', files={'file': open('fastapi/INMET_SE_RJ_A652_RIO DE JANEIRO - FORTE DE COPACABANA_01-01-2024_A_31-12-2024.CSV', 'rb')})"
```

5. **Acesse os serviços:**

- **JupyterLab:** http://localhost:8888 (sem token - acesso direto)
- **MLFlow:** http://localhost:5000
- **MinIO Console:** http://localhost:9001 (usuário: `minioadmin`, senha: `minioadmin`)
- **ThingsBoard:** http://localhost:8080 (usuário: `tenant@thingsboard.org`, senha: `tenant`)
- **FastAPI Docs:** http://localhost:8000/docs

## 📊 Fluxo de Trabalho

1. **Ingestão:** Upload do CSV via FastAPI → dados salvos no MinIO e PostgreSQL
2. **Tratamento:** Execute o notebook `01_tratamento_dados.ipynb` no JupyterLab
3. **Modelagem:** Execute o notebook `02_modelagem_temperatura.ipynb` para treinar modelos
4. **Visualização:** Execute o notebook `03_visualizacoes.ipynb` para gerar gráficos
5. **Monitoramento:** Acesse MLFlow para ver experimentos e métricas
6. **Dashboard:** Configure visualizações no ThingsBoard

## 📁 Estrutura do Repositório

```
/repo
├── docker-compose.yml          # Orquestração dos contêineres
├── fastapi/                     # API de ingestão
│   ├── Dockerfile
│   └── main.py
├── jupyterlab/                  # Ambiente de análise
│   └── Dockerfile
├── mlflow/                      # Versionamento de modelos
│   └── Dockerfile
├── notebooks/                   # Notebooks de análise
│   ├── 01_tratamento_dados.ipynb
│   ├── 02_modelagem_temperatura.ipynb
│   └── 03_visualizacoes.ipynb
├── sql_scripts/                 # Scripts SQL
│   ├── 01_create_tables.sql
│   └── 02_create_thingsboard_db.sql
├── upload_data.py               # Script auxiliar para upload de CSV
├── reports/                     # Relatórios e resultados
├── data/                        # Dados locais (volume)
└── README.md                    # Este arquivo
```

## 🔧 Comandos Úteis

### Ver logs dos serviços:
```bash
docker-compose logs -f [nome_servico]
```

### Parar todos os serviços:
```bash
docker-compose down
```

### Parar e remover volumes (limpar dados):
```bash
docker-compose down -v
```

### Reiniciar um serviço específico:
```bash
docker-compose restart [nome_servico]
```

### Verificar estatísticas da API:
```bash
curl http://localhost:8000/stats
```

## 📈 Modelos Implementados

- **Random Forest Regressor:** Modelo ensemble para regressão
- **Gradient Boosting Regressor:** Modelo de boosting para regressão

Métricas avaliadas:
- RMSE (Root Mean Squared Error)
- MAE (Mean Absolute Error)
- R² (Coeficiente de Determinação)

## 📝 Notas Importantes

- O primeiro acesso ao ThingsBoard pode demorar alguns minutos para inicializar
- Os dados são persistidos em volumes Docker, então não serão perdidos ao reiniciar
- O MinIO está configurado para usar credenciais padrão (altere em produção)
- O PostgreSQL cria automaticamente as tabelas via scripts em `sql_scripts/`
- **Dados do projeto:** Estação Forte de Copacabana (Rio de Janeiro), código A652, período 2024
- **JupyterLab:** Não requer token de autenticação (acesso direto)

## 🐛 Troubleshooting

**Problema:** Serviços não iniciam
- Solução: Verifique se as portas estão livres e se o Docker está rodando

**Problema:** Erro de conexão com PostgreSQL
- Solução: Aguarde alguns segundos após iniciar os serviços para o banco inicializar

**Problema:** JupyterLab não carrega
- Solução: Acesse http://localhost:8888 diretamente (sem token necessário)

**Problema:** ThingsBoard só mostra último valor
- Solução: Use a aba "Timeseries" (não "Última telemetria") e ajuste o filtro de tempo para incluir todo o período

**Problema:** Dados não aparecem no ThingsBoard
- Solução: Verifique se o access token está correto no notebook `03_visualizacoes.ipynb`
- Verifique se os dados foram enviados completamente (veja logs no notebook)

## 🔑 Credenciais Padrão

| Serviço | URL | Usuário | Senha/Token |
|---------|-----|---------|-------------|
| PostgreSQL | localhost:5432 | postgres | postgres |
| MinIO Console | http://localhost:9001 | minioadmin | minioadmin |
| ThingsBoard | http://localhost:8080 | tenant@thingsboard.org | tenant |
| JupyterLab | http://localhost:8888 | - | (sem autenticação) |
| MLFlow | http://localhost:5000 | - | - |
| FastAPI | http://localhost:8000 | - | - |

## 📚 Referências

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MLFlow Documentation](https://mlflow.org/docs/latest/index.html)
- [ThingsBoard Documentation](https://thingsboard.io/docs/)
- [MinIO Documentation](https://min.io/docs/)
- [INMET - Instituto Nacional de Meteorologia](https://portal.inmet.gov.br/)

## 📄 Licença

Este projeto está sob a licença MIT.


