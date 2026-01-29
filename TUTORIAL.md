# Tutorial: Conectando Python ao Astra DB (Cassandra)

Este tutorial documenta todos os passos necessários para configurar um projeto Python que se conecta ao Astra DB da DataStax.

---

## 📋 Pré-requisitos

- Python 3.8+
- Conta no [Astra DB](https://astra.datastax.com)
- Uma database criada no Astra DB

---

## 🚀 Passo 1: Criar a Estrutura do Projeto

```bash
# Criar diretório do projeto
mkdir teste-db-cassandra
cd teste-db-cassandra

# Inicializar repositório git (opcional)
git init
```

---

## 📦 Passo 2: Instalar Dependências

```bash
# Criar ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instalar pacotes necessários
pip install cassandra-driver
pip install python-dotenv
```

---

## 🔑 Passo 3: Obter Credenciais do Astra DB

1. Acesse o [Dashboard do Astra DB](https://astra.datastax.com)
2. Selecione sua database
3. Clique em **"Connect"**
4. Baixe o arquivo **`secure-connect-*.zip`** (arquivo de configuração)
   - Coloque este arquivo na raiz do seu projeto
5. Vá em **"Settings" → "Token Management"**
6. Crie um novo **Application Token** com permissões `Manage Keyspaces and Tables`
   - Copie o token (formato: `AstraCS:...`)
7. Identifique o **Keyspace** name (geralmente na seção "Details")

---

## ⚙️ Passo 4: Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```bash
# .env
ASTRA_DB_APPLICATION_TOKEN=AstraCS:seu_token_completo_aqui
```

**⚠️ Importante:** Adicione `.env` ao `.gitignore` para não expor credenciais:

```bash
echo ".env" >> .gitignore
```

---

## 📝 Passo 5: Criar o Arquivo de Conexão Principal (`app.py`)

```python
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
```

**Para testar a conexão:**
```bash
python app.py
```

---

## 🏫 Passo 6: Criar um Script com Operações CRUD (`escola.py`)

```python
import os
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from dotenv import load_dotenv
from datetime import datetime

# Carrega credenciais
load_dotenv()

def gerenciar_escola():
    cloud_config = {
        'secure_connect_bundle': 'secure-connect-app-test.zip'
    }
    
    # Usa Application Token
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
        
        # Especificar o keyspace
        session.set_keyspace('seu_keyspace_aqui')  # ⚠️ Mude para seu keyspace real

        # --- CRIAR TABELA ---
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

        # --- INSERIR DADOS ---
        query_insert = """
        INSERT INTO entregas_projetos (turma, id_aluno, nome_aluno, nome_projeto, nota, data_entrega)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

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
```

**Para executar:**
```bash
python escola.py
```

---

## ❌ Erros Comuns e Soluções

### 1. **`No such file or directory: 'secure-connect-*.zip'`**
- **Problema:** Arquivo de configuração não está no diretório do projeto
- **Solução:** Baixe o arquivo do Astra DB e coloque na raiz do projeto

### 2. **`Bad credentials` / `deprecated authentication`**
- **Problema:** Usando Client ID/Secret (método antigo)
- **Solução:** Use Application Token no formato `AstraCS:...`

### 3. **`No keyspace has been specified`**
- **Problema:** Não especificou qual keyspace usar
- **Solução:** Adicione `session.set_keyspace('seu_keyspace')`

### 4. **`ModuleNotFoundError: No module named 'cassandra'`**
- **Problema:** Dependências não instaladas
- **Solução:** Execute `pip install cassandra-driver python-dotenv`

---

## 📂 Estrutura Final do Projeto

```
teste-db-cassandra/
├── app.py                           # Script de teste de conexão
├── escola.py                        # Script com operações CRUD
├── .env                            # Credenciais (não versionado)
├── .gitignore                      # Ignora .env e venv
├── secure-connect-app-test.zip     # Arquivo de configuração do Astra DB
├── TUTORIAL.md                     # Este arquivo
└── venv/                           # Ambiente virtual
```

---

## ✅ Checklist de Configuração

- [ ] Python 3.8+ instalado
- [ ] Ambiente virtual criado e ativado
- [ ] `cassandra-driver` e `python-dotenv` instalados
- [ ] Conta no Astra DB criada
- [ ] Database no Astra DB criada
- [ ] Application Token gerado
- [ ] Arquivo `secure-connect-*.zip` baixado e colocado no projeto
- [ ] Arquivo `.env` criado com o token
- [ ] Arquivo `.env` adicionado ao `.gitignore`
- [ ] Keyspace identificado
- [ ] Scripts `app.py` e `escola.py` criados
- [ ] Conexão testada com sucesso

---

## 🔗 Referências Úteis

- [Astra DB Documentation](https://docs.datastax.com/en/astra-db-serverless/administration/intro.html)
- [Cassandra Python Driver](https://cassandra-python-driver.readthedocs.io/)
- [DataStax Token Management](https://docs.datastax.com/en/astra-db-serverless/administration/manage-application-tokens.html)

---

**Criado em:** 29 de Janeiro de 2026
