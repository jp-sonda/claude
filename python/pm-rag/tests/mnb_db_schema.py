import marimo

__generated_with = "0.17.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    > Construindo um sistema de **Text-to-SQL (ou NL2SQL)** utilizando Geração Aumentada por Recuperação (RAG) e embeddings.

    O desafio é traduzir a estrutura complexa de um **Schema de Banco de Dados** (JSON) para um formato otimizado para a pesquisa em um **Banco de Dados Vetorial** (Vector DB).

    Existe uma abordagem padrão para isso, mas ela requer uma etapa de processamento chamada **Chunking/Embedding Semântico**.

    ---

    ## 🚀 Abordagem Padrão para NL2SQL com Vector DBs

    A chave não é armazenar o JSON inteiro, mas sim **quebrar** o *schema* em fragmentos (chunks) que são semanticamente ricos e relevantes para responder a uma pergunta sobre o SQL.

    ### 1. Modelagem do Conhecimento (Chunking)

    O JSON do seu *schema* deve ser transformado em uma coleção de documentos textuais que descrevem as entidades e relações de forma compreensível para um Modelo de Linguagem Grande (LLM).

    O modelo padrão de *chunking* envolve a criação de documentos com diferentes níveis de granularidade:

    #### Chunk Type A: Descrição da Tabela (Mais Crítico)

    Crie um documento (texto) para **cada tabela** que inclua:

    * **Nome da Tabela:** `clients`
    * **Descrição da Tabela** (Se disponível no JSON).
    * **Colunas:** Uma lista formatada das colunas com seus tipos e descrições (*e.g.,* `client_id (INT, PK, Primary Key)`, `client_name (VARCHAR)`, `registration_date (DATE)`).
    * **Relacionamentos (FKs):** Qualquer chave estrangeira (FK) que esta tabela possui, junto com a tabela que ela referencia (*e.g.,* `FK: order_id references Orders.order_id`).

    > **Exemplo de Chunk A:**
    > `Tabela: Clientes. Colunas: client_id (INT, PK), client_name (VARCHAR). Descrição: Armazena dados de clientes. Relacionamentos: Nenhuma FK, mas é referenciada por Orders.client_id.`

    #### Chunk Type B: Descrição do Relacionamento (Crítico para Joins)

    Crie um documento separado para **cada relacionamento de chave estrangeira (FK)** no *schema*. Isso ajuda o LLM a entender como fazer *JOINs*.

    > **Exemplo de Chunk B:**
    > `Relacionamento: A tabela 'Orders' se relaciona com a tabela 'Clients' através da coluna Orders.client_id = Clients.client_id. Este é um relacionamento um-para-muitos.`

    #### Chunk Type C: Outros Metadados (Opcional, mas útil)

    Você pode incluir *chunks* para restrições específicas, índices (para indicar colunas importantes para filtros) ou valores de enumeração.

    ---

    ### 2. Geração e Armazenamento dos Embeddings

    1.  **Geração:** Use um **modelo de *embedding*** robusto (como `text-embedding-004` do Google, ou modelos open-source como `all-MiniLM-L6-v2`) para converter cada um dos *chunks* textuais (A, B, C) em um vetor numérico.
    2.  **Armazenamento:** Armazene esses vetores no seu Banco de Dados Vetorial (Pinecone, ChromaDB, Weaviate, etc.). Cada entrada no Vector DB será o vetor, o texto original do *chunk* e os metadados (como o nome da tabela).

    ---

    ### 3. Execução da Consulta NL2SQL (O Fluxo RAG)

    Quando o usuário faz uma pergunta em linguagem natural (e.g., **"Quantos pedidos o cliente João fez no último mês?"**):

    1.  **Embedding da Pergunta:** A pergunta é convertida em um vetor usando o **mesmo modelo de *embedding*** usado para o *schema*.
    2.  **Busca por Relevância (Retrieval):** O Vector DB é consultado para encontrar os *chunks* de *schema* mais relevantes (as tabelas, colunas e relacionamentos) que são semanticamente próximos à pergunta do usuário.
        * *Exemplo:* A busca recupera *chunks* sobre as tabelas `Clients`, `Orders` e o relacionamento entre elas.
    3.  **Geração do SQL (Augmentation):** O LLM (GPT-4, Gemini, etc.) recebe um **Prompt** contendo:
        * **Instruções:** "Você é um gerador de SQL. Sua tarefa é criar uma consulta SQL válida."
        * **Contexto Recuperado:** Os *chunks* do *schema* mais relevantes.
        * **Pergunta do Usuário (Query):** "Quantos pedidos o cliente João fez no último mês?"
    4.  **Saída:** O LLM usa o contexto do *schema* para gerar a consulta SQL correta.

    ---

    ## 💡 Modelo Padrão (Meta)

    Embora não haja um "formato de JSON" universalmente aceito para **entrada**, a **saída** para o Vector DB deve seguir esta estrutura para otimização do RAG:

    | Campo (Vector DB) | Tipo | Conteúdo / Propósito |
    | :--- | :--- | :--- |
    | **`vector`** | *Array* Numérico | O *embedding* do campo `text_chunk`. |
    | **`text_chunk`** | *String* | A descrição formatada (Chunk A, B ou C). |
    | **`chunk_type`** | Metadado | (`table`, `relationship`, `index`, etc.) |
    | **`source_table`** | Metadado | Nome da tabela principal descrita. |

    Ao usar essa estrutura, você garante que a recuperação (retrieval) no passo 3 seja eficiente e traga apenas o conhecimento necessário para o LLM gerar a SQL.

    ---
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Implementação""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Com um *schema* JSON bem estruturado podemos criar um *script* para processar o arquivo JSON, criar *chunks* (fragmentos) de conhecimento semanticamente ricos e gerar os *embeddings* usando um modelo eficiente, deixando tudo pronto para ser inserido no PostgreSQL com `pgvector`.

    ### 🛠️ Pré-requisitos (Instalação)

    Você precisará das seguintes bibliotecas:

    ```bash
    pip install pandas sentence-transformers numpy
    ```

    ### 🐍 Script Python para Geração de Chunks e Embeddings

    O script usa a biblioteca **Sentence Transformers** com o modelo `all-MiniLM-L6-v2` para gerar vetores de 384 dimensões.

    ```python
    import json
    import pandas as pd
    import numpy as np
    from sentence_transformers import SentenceTransformer

    # 1. Carregar o JSON do Schema
    schema_json = {
      "command": "describe-all",
      "timestamp": "2025-08-24T10:30:00",
      "database": "ecommerce_db",
      "schema": "public",
      "tables": {
        "users": {
          "columns": [
            {
              "column_name": "id",
              "data_type": "integer",
              "is_nullable": "NO"
            },
            {
              "column_name": "name",
              "data_type": "character varying",
              "is_nullable": "NO"
            },
            {
              "column_name": "email",
              "data_type": "character varying",
              "is_nullable": "YES"
            }
          ],
          "indexes": [
            {
              "index_name": "users_pkey",
              "column_name": "id",
              "is_unique": True,
              "is_primary": True
            }
          ],
          "constraints": [
            {
              "constraint_name": "users_pkey",
              "constraint_type": "PRIMARY KEY",
              "table_name": "users",
              "table_schema": "public",
              "column_name": "id"
            }
          ],
          "foreign_key_details": []
        },
        "categories": {
          "columns": [
            {
              "column_name": "id",
              "data_type": "integer",
              "is_nullable": "NO"
            },
            {
              "column_name": "name",
              "data_type": "character varying",
              "is_nullable": "NO"
            },
            {
              "column_name": "parent_id",
              "data_type": "integer",
              "is_nullable": "YES"
            }
          ],
          "indexes": [
            {
              "index_name": "categories_pkey",
              "column_name": "id",
              "is_unique": True,
              "is_primary": True
            }
          ],
          "constraints": [
            {
              "constraint_name": "categories_pkey",
              "constraint_type": "PRIMARY KEY",
              "table_name": "categories",
              "table_schema": "public",
              "column_name": "id"
            },
            {
              "constraint_name": "categories_parent_id_fkey",
              "constraint_type": "FOREIGN KEY",
              "table_name": "categories",
              "table_schema": "public",
              "column_name": "parent_id",
              "foreign_table_column": "public.categories.id"
            }
          ],
          "foreign_key_details": [
            {
              "constraint_name": "categories_parent_id_fkey",
              "column_name": "parent_id",
              "foreign_table_schema": "public",
              "foreign_table_name": "categories",
              "foreign_column_name": "id",
              "on_update": "NO ACTION",
              "on_delete": "SET NULL"
            }
          ]
        },
        "products": {
          "columns": [
            {
              "column_name": "id",
              "data_type": "integer",
              "is_nullable": "NO"
            },
            {
              "column_name": "name",
              "data_type": "character varying",
              "is_nullable": "NO"
            },
            {
              "column_name": "price",
              "data_type": "numeric",
              "is_nullable": "YES"
            },
            {
              "column_name": "category_id",
              "data_type": "integer",
              "is_nullable": "YES"
            }
          ],
          "indexes": [
            {
              "index_name": "products_pkey",
              "column_name": "id",
              "is_unique": True,
              "is_primary": True
            }
          ],
          "constraints": [
            {
              "constraint_name": "products_pkey",
              "constraint_type": "PRIMARY KEY",
              "table_name": "products",
              "table_schema": "public",
              "column_name": "id"
            },
            {
              "constraint_name": "products_category_id_fkey",
              "constraint_type": "FOREIGN KEY",
              "table_name": "products",
              "table_schema": "public",
              "column_name": "category_id",
              "foreign_table_column": "public.categories.id"
            }
          ],
          "foreign_key_details": [
            {
              "constraint_name": "products_category_id_fkey",
              "column_name": "category_id",
              "foreign_table_schema": "public",
              "foreign_table_name": "categories",
              "foreign_column_name": "id",
              "on_update": "NO ACTION",
              "on_delete": "SET NULL"
            }
          ]
        },
        "orders": {
          "columns": [
            {
              "column_name": "id",
              "data_type": "integer",
              "is_nullable": "NO"
            },
            {
              "column_name": "user_id",
              "data_type": "integer",
              "is_nullable": "NO"
            },
            {
              "column_name": "total",
              "data_type": "numeric",
              "is_nullable": "YES"
            },
            {
              "column_name": "order_date",
              "data_type": "timestamp",
              "is_nullable": "NO"
            }
          ],
          "indexes": [
            {
              "index_name": "orders_pkey",
              "column_name": "id",
              "is_unique": True,
              "is_primary": True
            }
          ],
          "constraints": [
            {
              "constraint_name": "orders_pkey",
              "constraint_type": "PRIMARY KEY",
              "table_name": "orders",
              "table_schema": "public",
              "column_name": "id"
            },
            {
              "constraint_name": "orders_user_id_fkey",
              "constraint_type": "FOREIGN KEY",
              "table_name": "orders",
              "table_schema": "public",
              "column_name": "user_id",
              "foreign_table_column": "public.users.id"
            }
          ],
          "foreign_key_details": [
            {
              "constraint_name": "orders_user_id_fkey",
              "column_name": "user_id",
              "foreign_table_schema": "public",
              "foreign_table_name": "users",
              "foreign_column_name": "id",
              "on_update": "NO ACTION",
              "on_delete": "CASCADE"
            }
          ]
        },
        "order_items": {
          "columns": [
            {
              "column_name": "id",
              "data_type": "integer",
              "is_nullable": "NO"
            },
            {
              "column_name": "order_id",
              "data_type": "integer",
              "is_nullable": "NO"
            },
            {
              "column_name": "product_id",
              "data_type": "integer",
              "is_nullable": "NO"
            },
            {
              "column_name": "quantity",
              "data_type": "integer",
              "is_nullable": "NO"
            },
            {
              "column_name": "price",
              "data_type": "numeric",
              "is_nullable": "NO"
            }
          ],
          "indexes": [
            {
              "index_name": "order_items_pkey",
              "column_name": "id",
              "is_unique": True,
              "is_primary": True
            }
          ],
          "constraints": [
            {
              "constraint_name": "order_items_pkey",
              "constraint_type": "PRIMARY KEY",
              "table_name": "order_items",
              "table_schema": "public",
              "column_name": "id"
            },
            {
              "constraint_name": "order_items_order_id_fkey",
              "constraint_type": "FOREIGN KEY",
              "table_name": "order_items",
              "table_schema": "public",
              "column_name": "order_id",
              "foreign_table_column": "public.orders.id"
            },
            {
              "constraint_name": "order_items_product_id_fkey",
              "constraint_type": "FOREIGN KEY",
              "table_name": "order_items",
              "table_schema": "public",
              "column_name": "product_id",
              "foreign_table_column": "public.products.id"
            }
          ],
          "foreign_key_details": [
            {
              "constraint_name": "order_items_order_id_fkey",
              "column_name": "order_id",
              "foreign_table_schema": "public",
              "foreign_table_name": "orders",
              "foreign_column_name": "id",
              "on_update": "NO ACTION",
              "on_delete": "CASCADE"
            },
            {
              "constraint_name": "order_items_product_id_fkey",
              "column_name": "product_id",
              "foreign_table_schema": "public",
              "foreign_table_name": "products",
              "foreign_column_name": "id",
              "on_update": "NO ACTION",
              "on_delete": "RESTRICT"
            }
          ]
        }
      },
      "show_constraints": True,
      "total_tables": 5,
      "failed_tables": []
    }

    # 2. Inicializar o modelo de embedding
    # 'all-MiniLM-L6-v2' gera embeddings de 384 dimensões, ideal para pgvector
    model_name = 'all-MiniLM-L6-v2'
    model = SentenceTransformer(model_name)
    EMBEDDING_DIMENSION = 384
    print(f"Modelo de Embedding carregado: {model_name}. Dimensão: {EMBEDDING_DIMENSION}")

    # Lista para armazenar todos os chunks (registros para o Vector DB)
    rag_records = []

    # Função para criar o chunk de descrição da Tabela (Chunk Type A)
    def create_table_chunk(table_name, table_data):
        # 1. Colunas e Chaves
        col_str = []
        for col in table_data['columns']:
            flags = []
            # Tenta inferir PK/FK a partir de índices e constraints
            if any(idx.get('is_primary') for idx in table_data.get('indexes', []) if idx.get('column_name') == col['column_name']):
                flags.append('PK')
            if any(fk.get('column_name') == col['column_name'] for fk in table_data.get('foreign_key_details', [])):
                flags.append('FK')

            flags_str = f" ({', '.join(flags)})" if flags else ""
            col_str.append(f"{col['column_name']} ({col['data_type']}){flags_str}")

        columns_list = "; ".join(col_str)

        # 2. Relacionamentos
        fk_list = []
        for fk in table_data['foreign_key_details']:
            target_col = f"{fk['foreign_table_name']}.{fk['foreign_column_name']}"
            fk_list.append(f"Chave Estrangeira: A coluna '{fk['column_name']}' referencia '{target_col}' (Constraint: {fk['on_delete']})")

        relationships_str = "\n".join(fk_list) if fk_list else "Sem chaves estrangeiras de saída."

        # 3. Monta o texto final do chunk
        text_chunk = (
            f"Tabela: **{table_name}**.\n"
            f"Descrição: {table_name.capitalize()} armazena dados de {table_name.replace('_', ' ').lower()}.\n"
            f"Colunas (Nome | Tipo | Restrições): {columns_list}.\n"
            f"Relacionamentos: {relationships_str}"
        )

        return {
            'text_chunk': text_chunk,
            'chunk_type': 'table_description',
            'source_table': table_name
        }

    # Função para criar o chunk de Relacionamento (Chunk Type B)
    def create_relationship_chunk(fk_detail, source_table_name):
        # Formata a string de relacionamento para ser otimizada para JOIN

        source_col = fk_detail['column_name']
        target_table = fk_detail['foreign_table_name']
        target_col = fk_detail['foreign_column_name']

        text_chunk = (
            f"RELACIONAMENTO: Para fazer JOIN (ligação) entre a tabela **{source_table_name}** e a tabela **{target_table}**, use a coluna {source_table_name}.{source_col} "
            f"que deve ser igual a {target_table}.{target_col}. "
            f"(Exemplo: SELECT * FROM {source_table_name} JOIN {target_table} ON {source_table_name}.{source_col} = {target_table}.{target_col})"
        )

        return {
            'text_chunk': text_chunk,
            'chunk_type': 'relationship_join',
            'source_table': source_table_name,
            'target_table': target_table 
        }

    # 3. Processamento e Geração de Chunks

    for table_name, table_data in schema_json['tables'].items():
        # --- Chunk A: Descrição da Tabela ---
        table_chunk = create_table_chunk(table_name, table_data)
        rag_records.append(table_chunk)

        # --- Chunk B: Relacionamento ---
        for fk in table_data['foreign_key_details']:
            relationship_chunk = create_relationship_chunk(fk, table_name)
            rag_records.append(relationship_chunk)

    # 4. Geração dos Embeddings e Finalização do DataFrame

    # Extrai todos os chunks de texto
    texts_to_embed = [record['text_chunk'] for record in rag_records]

    # Gera os embeddings em lote
    print("\nGerando embeddings para todos os chunks...")
    embeddings = model.encode(texts_to_embed, convert_to_tensor=False)
    print("Embeddings gerados.")

    # Adiciona os vetores à lista de registros
    for i, record in enumerate(rag_records):
        # Converte o array numpy para o formato de string de lista, ideal para inserção SQL/pgvector
        record['vector'] = list(embeddings[i].astype(np.float32))

    # Cria o DataFrame final no formato pgvector/RAG
    df_rag_table = pd.DataFrame(rag_records)

    # Reordena e limpa as colunas para o formato final
    df_rag_table = df_rag_table[['vector', 'text_chunk', 'chunk_type', 'source_table', 'target_table']]
    df_rag_table = df_rag_table.fillna('') # Limpa o campo target_table onde não se aplica

    # 5. Saída e Visualização
    print("\n--- Estrutura Final da Tabela RAG (Apenas Primeiras Linhas) ---")
    print(df_rag_table.head())
    print(f"\nTotal de registros RAG gerados: {len(df_rag_table)}")
    print(f"Dimensão do vetor: {len(df_rag_table['vector'].iloc[0])}")

    # Exemplo de como o Chunk A (users) ficou:
    print("\n--- Exemplo de Chunk (Tabela 'users') ---")
    print(df_rag_table[df_rag_table['source_table'] == 'users']['text_chunk'].iloc[0])

    # Exemplo de Chunk B (orders -> users)
    print("\n--- Exemplo de Chunk (Relacionamento 'orders' -> 'users') ---")
    print(df_rag_table[df_rag_table['source_table'] == 'orders']['text_chunk'].iloc[1])
    ```

    -----

    ### 📝 Estrutura para Inserção no PostgreSQL com `pgvector`

    O `DataFrame` final (`df_rag_table`) tem a estrutura ideal para ser inserido no PostgreSQL.

    #### 1\. SQL para Criar a Tabela Vetorial

    Primeiro, você deve criar a tabela no seu banco de dados PostgreSQL. O tipo de dado **`vector`** é fornecido pela extensão `pgvector`.

    ```sql
    -- Habilite a extensão pgvector (se ainda não estiver habilitada)
    CREATE EXTENSION IF NOT EXISTS vector;

    -- Crie a tabela para armazenar o conhecimento do Schema
    CREATE TABLE schema_rag_chunks (
        id SERIAL PRIMARY KEY,
        vector VECTOR(384),  -- A dimensão do seu embedding (384 no nosso exemplo)
        text_chunk TEXT NOT NULL,
        chunk_type VARCHAR(50) NOT NULL,
        source_table VARCHAR(50) NOT NULL,
        target_table VARCHAR(50)
    );
    ```

    #### 2\. Inserção dos Dados

    Você pode usar o Pandas com uma biblioteca como `psycopg2` ou `sqlalchemy` para conectar ao PostgreSQL e inserir o `df_rag_table`.

    ```python
    # Exemplo de inserção (apenas conceito, pois requer credenciais do DB)

    import psycopg2

    # Configurações de conexão
    DB_HOST = "localhost"
    DB_NAME = "ecommerce_db"
    DB_USER = "seu_usuario"
    DB_PASSWORD = "sua_senha"

    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()

    for index, row in df_rag_table.iterrows():
        # Formata o vetor como uma string compatível com ARRAY do PostgreSQL, se necessário.
        # Se você estiver usando ORMs modernos ou bibliotecas atualizadas, o objeto list(vector)
        # pode ser inserido diretamente no campo VECTOR.
        vector_str = "[" + ",".join(map(str, row['vector'])) + "]"

        insert_query = f\"""
        INSERT INTO schema_rag_chunks (vector, text_chunk, chunk_type, source_table, target_table)
        VALUES (%s, %s, %s, %s, %s);
        \"""

        cursor.execute(insert_query, (
            vector_str,
            row['text_chunk'],
            row['chunk_type'],
            row['source_table'],
            row['target_table']
        ))

    conn.commit()
    cursor.close()
    conn.close()

    ```

    Agora você tem todos os metadados do seu *schema* convertidos em vetores e prontos para serem buscados semanticamente para alimentar um LLM na geração de consultas SQL em linguagem natural.
    """
    )
    return


if __name__ == "__main__":
    app.run()
