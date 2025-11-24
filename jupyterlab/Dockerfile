FROM jupyter/scipy-notebook:latest

USER root

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

USER jovyan

# Instala pacotes Python adicionais
RUN pip install --no-cache-dir \
    psycopg2-binary==2.9.9 \
    minio==7.2.0 \
    boto3==1.29.7 \
    mlflow==2.8.1 \
    scikit-learn==1.3.2 \
    matplotlib==3.8.2 \
    seaborn==0.13.0 \
    plotly==5.18.0 \
    pandas==2.1.3 \
    numpy==1.26.2 \
    sqlalchemy==2.0.23

# Copia configuração do Jupyter
COPY jupyter_lab_config.py /home/jovyan/.jupyter/jupyter_lab_config.py

# Configura variáveis de ambiente para MLFlow S3
ENV MLFLOW_S3_ENDPOINT_URL=http://minio:9000
ENV AWS_ACCESS_KEY_ID=minioadmin
ENV AWS_SECRET_ACCESS_KEY=minioadmin
ENV AWS_DEFAULT_REGION=us-east-1

WORKDIR /home/jovyan/work

