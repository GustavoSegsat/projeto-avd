-- Script de criação de tabelas para dados meteorológicos

-- Tabela principal de dados meteorológicos
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

-- Índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_datetime ON dados_meteorologicos(datetime);
CREATE INDEX IF NOT EXISTS idx_data ON dados_meteorologicos(data);
CREATE INDEX IF NOT EXISTS idx_temperatura ON dados_meteorologicos(temperatura);

-- Tabela para predições de temperatura
CREATE TABLE IF NOT EXISTS predicoes_temperatura (
    id SERIAL PRIMARY KEY,
    datetime TIMESTAMP NOT NULL,
    temperatura_real FLOAT,
    temperatura_predita FLOAT,
    modelo_version VARCHAR(50),
    rmse FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_pred_datetime ON predicoes_temperatura(datetime);

-- View para análise exploratória
CREATE OR REPLACE VIEW vw_estatisticas_diarias AS
SELECT 
    DATE(datetime) as data,
    COUNT(*) as total_registros,
    AVG(temperatura) as temp_media,
    MIN(temperatura) as temp_min,
    MAX(temperatura) as temp_max,
    AVG(umidade) as umidade_media,
    AVG(pressao) as pressao_media,
    SUM(precipitacao) as precipitacao_total,
    AVG(vento_velocidade) as vento_medio
FROM dados_meteorologicos
GROUP BY DATE(datetime)
ORDER BY data DESC;


