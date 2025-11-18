FROM python:3.11-slim

WORKDIR /mlflow

RUN apt-get update && apt-get install -y \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    mlflow==2.8.1 \
    psycopg2-binary==2.9.9 \
    boto3==1.29.7 \
    minio==7.2.0

COPY init_minio.sh /mlflow/init_minio.sh
RUN chmod +x /mlflow/init_minio.sh

# Configura MinIO como backend S3 para MLFlow
ENV MLFLOW_S3_ENDPOINT_URL=http://minio:9000
ENV AWS_ACCESS_KEY_ID=minioadmin
ENV AWS_SECRET_ACCESS_KEY=minioadmin
ENV AWS_DEFAULT_REGION=us-east-1
ENV MLFLOW_S3_IGNORE_TLS=true

EXPOSE 5000

# Inicializa buckets e inicia MLFlow
CMD /mlflow/init_minio.sh & \
    mlflow server \
     --backend-store-uri postgresql://postgres:postgres@postgres:5432/inmet_db \
     --default-artifact-root s3://mlflow-artifacts/ \
     --host 0.0.0.0 \
     --port 5000

