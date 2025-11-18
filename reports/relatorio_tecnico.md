# Relatório Técnico - Pipeline de Análise e Visualização de Dados Meteorológicos

## 1. Introdução e Objetivos

### 1.1 Contexto

Este projeto desenvolve um pipeline completo de análise e visualização de dados meteorológicos coletados do INMET (Instituto Nacional de Meteorologia), especificamente para a estação de Recife (PE), código A301, no período de 2021.

### 1.2 Objetivos

O objetivo principal é **prever a temperatura horária** com base em variáveis meteorológicas históricas, utilizando técnicas de aprendizado de máquina e disponibilizando os resultados através de dashboards interativos.

Objetivos específicos:
- Implementar um pipeline de ingestão de dados via FastAPI
- Armazenar dados brutos em MinIO (S3-compatible) e estruturados em PostgreSQL
- Realizar tratamento e limpeza de dados
- Desenvolver modelos preditivos de regressão
- Versionar modelos no MLFlow
- Visualizar dados e predições no ThingsBoard

## 2. Arquitetura e Ferramentas

### 2.1 Arquitetura do Sistema

O pipeline segue uma arquitetura em camadas:

```
┌─────────────┐
│   CSV INMET │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   FastAPI   │ ──► MinIO (S3) ──► Dados Brutos
│  (Ingestão) │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ PostgreSQL  │ ──► Dados Estruturados
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ JupyterLab  │ ──► Tratamento + Modelagem
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   MLFlow    │ ──► Versionamento de Modelos
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ ThingsBoard │ ──► Dashboards e Visualizações
└─────────────┘
```

### 2.2 Ferramentas Utilizadas

| Ferramenta | Versão | Função |
|------------|--------|--------|
| FastAPI | 0.104.1 | API REST para ingestão |
| MinIO | Latest | Armazenamento de objetos (S3) |
| PostgreSQL | 15 | Banco de dados relacional |
| JupyterLab | Latest | Ambiente de análise |
| MLFlow | 2.8.1 | Versionamento de modelos |
| ThingsBoard | Latest | Dashboard IoT |
| Python | 3.11 | Linguagem principal |
| scikit-learn | 1.3.2 | Machine Learning |
| pandas | 2.1.3 | Manipulação de dados |

### 2.3 Orquestração

Todos os serviços são orquestrados via Docker Compose, garantindo:
- Isolamento de ambientes
- Facilidade de deploy
- Consistência entre ambientes
- Escalabilidade

## 3. Metodologia de Tratamento e Modelagem

### 3.1 Coleta de Dados

Os dados são coletados do arquivo CSV do INMET contendo:
- **Período:** 01/01/2021 a 31/12/2021
- **Frequência:** Horária
- **Estação:** Recife (A301)
- **Variáveis:** Temperatura, Umidade, Pressão, Radiação, Vento, Precipitação

### 3.2 Ingestão

O FastAPI recebe o arquivo CSV e:
1. Faz parse do arquivo (pulando cabeçalho da estação)
2. Trata encoding (Latin-1)
3. Converte tipos de dados
4. Salva no MinIO (dados brutos)
5. Insere no PostgreSQL (dados estruturados)

### 3.3 Tratamento e Limpeza

#### 3.3.1 Remoção de Dados Inválidos
- Remoção de registros completamente vazios
- Validação de timestamps

#### 3.3.2 Tratamento de Valores Faltantes
- Interpolação linear temporal para variáveis contínuas
- Preservação da ordem temporal dos dados

#### 3.3.3 Detecção e Remoção de Outliers
- Método IQR (Interquartile Range) para temperatura
- Limites: Q1 - 1.5×IQR e Q3 + 1.5×IQR

#### 3.3.4 Feature Engineering
- Features temporais: ano, mês, dia, hora, dia da semana, dia do ano
- Features cíclicas: seno/cosseno de hora e mês (para capturar padrões sazonais)

### 3.4 Modelagem

#### 3.4.1 Preparação dos Dados
- **Features:** Umidade, Pressão, Radiação, Vento (direção e velocidade), Precipitação, Features temporais
- **Target:** Temperatura horária
- **Split:** 80% treino / 20% teste (temporal, preservando ordem)

#### 3.4.2 Modelos Implementados

**1. Random Forest Regressor**
- n_estimators: 100
- max_depth: 15
- min_samples_split: 5

**2. Gradient Boosting Regressor**
- n_estimators: 100
- max_depth: 5
- learning_rate: 0.1

#### 3.4.3 Métricas de Avaliação
- **RMSE:** Root Mean Squared Error
- **MAE:** Mean Absolute Error
- **R²:** Coeficiente de Determinação

## 4. Análises e Resultados

### 4.1 Estatísticas Descritivas

[Inserir aqui estatísticas descritivas dos dados após tratamento]

### 4.2 Resultados dos Modelos

[Inserir aqui tabela comparativa dos modelos com métricas]

### 4.3 Análise de Importância de Features

[Inserir gráfico de importância das features]

### 4.4 Visualizações

#### 4.4.1 Série Temporal
[Inserir gráfico da série temporal de temperatura]

#### 4.4.2 Real vs Predito
[Inserir gráfico comparando valores reais e preditos]

#### 4.4.3 Distribuição de Erros
[Inserir histograma dos erros de predição]

## 5. Dashboard e Insights

### 5.1 ThingsBoard

[Descrever configuração do dashboard no ThingsBoard]

### 5.2 Insights Obtidos

[Inserir insights principais obtidos da análise]

## 6. Conclusões e Melhorias Futuras

### 6.1 Conclusões

[Inserir conclusões do projeto]

### 6.2 Melhorias Futuras

- Implementar modelos de séries temporais (LSTM, Prophet)
- Adicionar mais variáveis meteorológicas
- Implementar predição multi-horizonte
- Melhorar tratamento de dados faltantes com métodos mais sofisticados
- Adicionar monitoramento em tempo real
- Implementar retreinamento automático de modelos

## 7. Referências

- INMET - Instituto Nacional de Meteorologia
- Documentação FastAPI
- Documentação MLFlow
- Documentação ThingsBoard
- Scikit-learn Documentation

---

**Data de Entrega:** 04/12/2024  
**Versão:** 1.0


