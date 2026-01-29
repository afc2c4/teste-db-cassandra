import os
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

def conectar_cassandra():
    cloud_config = {
        'secure_connect_bundle': 'secure-connect-app-test.zip'  # Mude para o nome exato do seu arquivo
    }

    # Usa Application Token (formato: AstraCS:...)
    token = os.getenv('ASTRA_DB_APPLICATION_TOKEN')
    auth_provider = PlainTextAuthProvider(
        username='token',
        password=token
    )

    try:
        cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
        session = cluster.connect()

        row = session.execute("select release_version from system.local").one()
        if row:
            print(f"Sucesso! Conectado ao Cassandra versão: {row[0]}")
        else:
            print("Conectado, mas nenhum dado retornado.")

    except Exception as e:
        print(f"Erro ao conectar: {e}")

if __name__ == "__main__":
    conectar_cassandra()