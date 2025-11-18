FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    fastapi==0.104.1 \
    uvicorn==0.24.0 \
    minio==7.2.0 \
    psycopg2-binary==2.9.9 \
    pandas==2.1.3 \
    python-multipart==0.0.6

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


