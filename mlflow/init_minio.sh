#!/bin/bash
# Script para inicializar buckets no MinIO

echo "Aguardando MinIO estar disponível..."
sleep 10

# Instala mc (MinIO Client) se necessário
if ! command -v mc &> /dev/null; then
    echo "Instalando MinIO Client..."
    wget -q https://dl.min.io/client/mc/release/linux-amd64/mc -O /tmp/mc
    chmod +x /tmp/mc
    MC=/tmp/mc
else
    MC=mc
fi

# Configura acesso ao MinIO
$MC alias set minio http://minio:9000 minioadmin minioadmin

# Cria bucket para MLFlow artifacts
$MC mb minio/mlflow-artifacts --ignore-existing || true
$MC anonymous set download minio/mlflow-artifacts || true

echo "Buckets criados com sucesso!"


