#!/usr/bin/env python3
"""
Script auxiliar para fazer upload do arquivo CSV para a API FastAPI
"""
import requests
import sys
import os

def upload_csv(file_path, api_url="http://localhost:8000/upload"):
    """Faz upload do arquivo CSV para a API"""
    if not os.path.exists(file_path):
        print(f"Erro: Arquivo não encontrado: {file_path}")
        return False
    
    try:
        print(f"Fazendo upload de {file_path}...")
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f, 'text/csv')}
            response = requests.post(api_url, files=files)
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Upload realizado com sucesso!")
            print(f"   Arquivo: {result.get('filename')}")
            print(f"   Registros: {result.get('records')}")
            print(f"   Período: {result.get('date_range', {}).get('start')} a {result.get('date_range', {}).get('end')}")
            return True
        else:
            print(f"❌ Erro no upload: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar à API.")
        print("   Certifique-se de que o FastAPI está rodando (docker-compose up)")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        csv_file = "INMET_NE_PE_A301_RECIFE_01-01-2021_A_31-12-2021.CSV"
        if not os.path.exists(csv_file):
            print("Uso: python upload_data.py <caminho_do_arquivo.csv>")
            sys.exit(1)
    else:
        csv_file = sys.argv[1]
    
    success = upload_csv(csv_file)
    sys.exit(0 if success else 1)


