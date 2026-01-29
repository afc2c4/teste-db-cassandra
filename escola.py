import os
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from dotenv import load_dotenv
from datetime import datetime

# 1. Carregar credenciais
load_dotenv()

def gerenciar_escola():
    # Configuração de conexão (igual ao anterior)
    cloud_config = {
        'secure_connect_bundle': 'secure-connect-app-test.zip'  # Verifique o nome do arquivo!
    }
    
    # Usa Application Token (formato: AstraCS:...)
    token = os.getenv('ASTRA_DB_APPLICATION_TOKEN')
    auth_provider = PlainTextAuthProvider(
        username='token',
        password=token
    )

    try:
        # Conectar
        print("Conectando ao banco da escola...")
        cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
        session = cluster.connect()
        
        # Especificar o keyspace (substitua 'seu_keyspace' pelo nome do seu keyspace no Astra DB)
        session.set_keyspace('entrega_trabalho')  # Altere para o seu keyspace

        # --- PARTE A: CRIAR A TABELA (CREATE) ---
        # Contexto: Tabela para guardar notas de projetos por turma.
        # PRIMARY KEY explained:
        # 'turma' é a Partition Key (agrupa os dados fisicamente por turma).
        # 'id_aluno' é a Clustering Key (ordena os alunos dentro daquela turma).

        create_table_query = """
        CREATE TABLE IF NOT EXISTS entregas_projetos (
            turma text,
            id_aluno int,
            nome_aluno text,
            nome_projeto text,
            nota float,
            data_entrega timestamp,
            PRIMARY KEY (turma, id_aluno)
        );
        """
        session.execute(create_table_query)
        print("Tabela 'entregas_projetos' criada (ou já existia).")

        # --- PARTE B: INSERIR DADOS (INSERT) ---
        # Vamos inserir 3 alunos fictícios de uma turma de "Front-End"

        query_insert = """
        INSERT INTO entregas_projetos (turma, id_aluno, nome_aluno, nome_projeto, nota, data_entrega)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        # Dados simulados
        dados_alunos = [
            ("Técnico_ADS_2026", 101, "Carlos Silva", "Sistema de Biblioteca", 9.5, datetime.now()),
            ("Técnico_ADS_2026", 102, "Ana Souza", "E-commerce de Roupas", 8.0, datetime.now()),
            ("Técnico_Redes_2026", 201, "Marcos Paulo", "Configuração Firewall", 10.0, datetime.now())
        ]

        for dado in dados_alunos:
            session.execute(query_insert, dado)
            print(f"Nota do aluno {dado[2]} registrada com sucesso!")

    except Exception as e:
        print(f"Erro no sistema escolar: {e}")

if __name__ == "__main__":
    gerenciar_escola()