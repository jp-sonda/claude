import os
import yaml # Importe a biblioteca PyYAML
from typing import Optional, Any
from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import reflection
from pydantic import BaseModel, Field

"""
No caso de usar psql -h localhost -p 54320 -U dcnr dcnrh # com senha cepel e schema dcnrapp
preencha assim o script para setar as variáveis de ambiente:

export POSTGRES_USER=dcnr
export POSTGRES_PASSWORD=cepel
export POSTGRES_HOST=localhost
export POSTGRES_PORT=54320
export POSTGRES_DB=dcnrh
export POSTGRES_TARGET_SCHEMA=dcnrapp

E teste assim:
echo POSTGRES_USER = $POSTGRES_USER
echo POSTGRES_PASSWORD = $POSTGRES_PASSWORD
echo POSTGRES_HOST = $POSTGRES_HOST
echo POSTGRES_PORT = $POSTGRES_PORT
echo POSTGRES_DB = $POSTGRES_DB
echo POSTGRES_TARGET_SCHEMA = $POSTGRES_TARGET_SCHEMA
"""

CAN_PRINT_TABLE_STRUCTURE = False

# --- 1. Configuração do Banco de Dados ---
# Recomenda-se usar variáveis de ambiente ou um arquivo de configuração seguro
POSTGRES_USER = os.getenv("POSTGRES_USER", "NONE")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "NONE") # Altere para sua senha
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "NONE")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "NONE")
POSTGRES_DB = os.getenv("POSTGRES_DB", "NONE") # Altere para o nome do seu banco de dados
POSTGRES_TARGET_SCHEMA = os.getenv("POSTGRES_TARGET_SCHEMA", "NONE")

# String de conexão PostgreSQL
DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
TARGET_SCHEMA = POSTGRES_TARGET_SCHEMA # O schema que você deseja inspecionar

# --- 2. Modelos Pydantic para Descrever o Esquema ---

class ColumnSchema(BaseModel):
    """Representa a descrição de uma coluna da tabela."""
    column_name: str
    type: str
    nullable: bool
    default: Optional[str] = None
    autoincrement: Optional[bool] = False

class PrimaryKeySchema(BaseModel):
    """Representa a chave primária de uma tabela."""
    constrained_columns: list[str]

class IndexSchema(BaseModel):
    """Representa um índice de uma tabela."""
    index_name: Optional[str] = None
    column_names: list[Optional[str]]
    unique: bool

class ForeignKeySchema(BaseModel):
    """Representa uma chave estrangeira."""
    constrained_columns: list[str]
    referred_table: str
    referred_columns: list[str]
    name: Optional[str] = None
    ondelete: Optional[str] = None
    onupdate: Optional[str] = None

class TableSchema(BaseModel):
    """Representa a descrição completa de uma tabela."""
    table_name: str
    schema_name: str
    columns: list[ColumnSchema]
    primary_key: Optional[PrimaryKeySchema] = None
    indexes: list[IndexSchema] = Field(default_factory=list)
    foreign_keys: list[ForeignKeySchema] = Field(default_factory=list)
    # Adicionar metadados adicionais, se necessário
    # options: dict[str, Any] # Ex: para tabelas específicas do PG, como 'oids'

# --- 3. Lógica de Introspecção e Mapeamento ---

def inspect_database_schema(db_url: str, schema_name: str) -> list[TableSchema]:
    """
    Conecta-se ao banco de dados, inspeciona o schema especificado
    e retorna uma lista de objetos TableSchema.
    """
    try:
        engine = create_engine(db_url)
        inspector = inspect(engine)

        # Valida se o schema existe
        if schema_name not in inspector.get_schema_names():
            print(f"Erro: O schema '{schema_name}' não foi encontrado no banco de dados.")
            return []

        all_tables_schema: list[TableSchema] = []

        print(f"Inspecionando tabelas no schema: '{schema_name}'...")
        table_count = 0
    
        # Obter nomes das tabelas no schema
        table_names = inspector.get_table_names(schema=schema_name)

        for table_name in table_names:
            table_count = table_count + 1
            print(f"{table_count}\tProcessando tabela: {table_name}")

            # 1. Obter informações das colunas
            columns_info = inspector.get_columns(table_name, schema=schema_name)
            columns_info.sort(key=lambda column: column['name'])
            columns = [
                ColumnSchema(
                    column_name=col['name'],
                    type=str(col['type']), # Converte o tipo do SQLAlchemy para string
                    nullable=col['nullable'],
                    default=col['default'],
                    autoincrement=col.get('autoincrement')
                )
                for col in columns_info
            ]

            # 2. Obter informações da chave primária
            pk_info = inspector.get_pk_constraint(table_name, schema=schema_name)
            primary_key = None
            if pk_info and pk_info.get('constrained_columns'):
                primary_key = PrimaryKeySchema(constrained_columns=pk_info['constrained_columns'])

            # 3. Obter informações dos índices
            indexes_info = inspector.get_indexes(table_name, schema=schema_name)
            indexes = [
                IndexSchema(
                    index_name=idx['name'],
                    column_names=idx['column_names'],
                    unique=idx['unique']
                )
                for idx in indexes_info
            ]

            # 4. Obter informações das chaves estrangeiras
            fks_info = inspector.get_foreign_keys(table_name, schema=schema_name)
            foreign_keys = [
                ForeignKeySchema(
                    constrained_columns=fk['constrained_columns'],
                    referred_table=fk['referred_table'],
                    referred_columns=fk['referred_columns'],
                    name=fk.get('name'),
                    ondelete=fk.get('ondelete'),
                    onupdate=fk.get('onupdate')
                )
                for fk in fks_info
            ]

            # Criar o objeto TableSchema para a tabela atual
            table_schema_obj = TableSchema(
                table_name=table_name,
                schema_name=schema_name,
                columns=columns,
                primary_key=primary_key,
                indexes=indexes,
                foreign_keys=foreign_keys
            )
            all_tables_schema.append(table_schema_obj)

    except Exception as e:
        print(f"Ocorreu um erro ao inspecionar o banco de dados: {e}")
        return []
    finally:
        engine.dispose() # Garante que a conexão seja fechada

    # Ordenando a lista de tabelas pelo atributo table_name
    all_tables_schema.sort(key=lambda table: table.table_name)
    print(f"Foram processadas {table_count} tabelas no schema {POSTGRES_TARGET_SCHEMA} do database {DATABASE_URL}")
    return all_tables_schema

# --- Nova Função para Gerar YAML ---

def generate_yaml_from_tables_schema(tables_schema: list[TableSchema], output_filename: str = "database_schema.yaml"):
    """
    Recebe uma lista de objetos TableSchema e gera um arquivo YAML.
    """
    if not tables_schema:
        print("Nenhum dado de tabela para gerar o arquivo YAML.")
        return

    # Converte a lista de modelos Pydantic para uma lista de dicionários Python
    # O método .model_dump() do Pydantic (ou .dict() em versões mais antigas)
    # converte o modelo em um dicionário compatível com serialização.
    data_to_serialize = [table.model_dump(mode='json') for table in tables_schema]

    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            yaml.dump(data_to_serialize, f, allow_unicode=True, sort_keys=False, indent=2)
        print(f"\nArquivo '{output_filename}' gerado com sucesso!")
    except Exception as e:
        print(f"Erro ao gerar o arquivo YAML: {e}")

def print_table_structure():
    for table in tables_description:
        print(f"\n## Tabela: {table.table_name} (Schema: {table.schema_name})")

        print("\n  Colunas:")
        for col in table.columns:
            print(f"    - {col.column_name}: {col.type} {'(NOT NULL)' if not col.nullable else ''} {'(Default: ' + col.default + ')' if col.default else ''} {'(AutoIncrement)' if col.autoincrement else ''}")

        if table.primary_key:
            print(f"\n  Chave Primária: {', '.join(table.primary_key.constrained_columns)}")

        if table.indexes:
            print("\n  Índices:")
            for idx in table.indexes:
                print(f"    - {idx.index_name}: Colunas={', '.join(idx.column_names)} {'(Único)' if idx.unique else ''}")

        if table.foreign_keys:
            print("\n  Chaves Estrangeiras:")
            for fk in table.foreign_keys:
                constrained_cols = ', '.join(fk.constrained_columns)
                referred_cols = ', '.join(fk.referred_columns)
                print(f"    - {fk.name if fk.name else 'FK'}: ({constrained_cols}) Referencia {fk.referred_table}({referred_cols})")

# --- Execução Principal ---
# print("\n\nPrograma carregado")
if __name__ == "__main__":
    print("\nIniciando a introspecção do banco de dados...")

    tables_description: list[TableSchema] = inspect_database_schema(DATABASE_URL, POSTGRES_TARGET_SCHEMA)

    if tables_description:
        # Chama a função para gerar o arquivo YAML
        generate_yaml_from_tables_schema(tables_description, f"{TARGET_SCHEMA}_schema.yaml")
        if CAN_PRINT_TABLE_STRUCTURE:
            print(f"\n--- Estrutura das Tabelas no Schema '{POSTGRES_TARGET_SCHEMA}' ---")
            print_table_structure()
    else:
        print("Nenhuma tabela encontrada ou erro na introspecção.")

    print(f"\nFim do Programa. Veja o arquivo {TARGET_SCHEMA}_schema.yaml")
