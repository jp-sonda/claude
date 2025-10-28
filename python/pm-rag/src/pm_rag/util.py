from typing import override, final, Optional, Sequence, Any
import sys
from pathlib import Path
import psycopg
from pandas import DataFrame
from pgvector.psycopg import register_vector
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.engine import Row
from sqlalchemy.engine.cursor import CursorResult
import numpy as np
import pandas as pd

import subprocess

pd.set_option('display.max_columns', None)  # para mostrar um número ilimitado de colunas
pd.set_option('display.max_rows', None)  # para mostrar todas as linhas
pd.set_option('display.width', 2000)  # Configura a largura da tela para um valor arbitrariamente grande

ENHANCEDS = ["get_maintenance_text"]
SQL_COMMANDS = {
    "get_maintenance_text": """select equipment_number as equip, functional_location as loc, order_type, maintenance_text
    from sap_pm_rag_data order by 1, 2
    """,
    "get_distinct_order_type": """select distinct equipment_number, functional_location, order_type
    from sap_pm_rag_data order by 1, 2
    """,
    "equipment_maintainance_priority": """
    -- Equipamentos com mais falhas corretivas vs preventivas
    SELECT
        equipment_number,
        COUNT(CASE WHEN order_type = 'PM01' THEN 1 END) as corretivas,
        COUNT(CASE WHEN order_type = 'PM03' THEN 1 END) as preventivas
    FROM sap_pm_rag_data
    GROUP BY equipment_number
    ORDER BY 2 DESC, 3 DESC, 1 ASC;
    """,
}

# Configurações de conexão com o PostgreSQL
DB_CONFIG = {
    "host": "localhost",
    "port": 5434,
    "dbname": "postgres",  # "pm_rag",
    "user": "postgres",  # "postgres",
    "password": "allsecret",
}


def create_psycopg_connection():
    """
    Cria e retorna uma conexão psycopg com pgvector registrado

    Returns:
        psycopg.Connection: Conexão ativa com o PostgreSQL

    Raises:
        Exception: Se houver erro na conexão
    """
    conn_string = get_connection_string()
    conn = None

    try:
        conn = psycopg.connect(conn_string)
        register_vector(conn)
        return conn
    except Exception as e:
        if conn:
            conn.close()
        raise Exception(f"Erro ao criar conexão psycopg: {e}")


def get_connection_string():
    """Retorna a string de conexão do PostgreSQL"""
    return f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"


def get_sqlalchemy_connection_string():
    """Retorna a string de conexão do PostgreSQL para SQLAlchemy com psycopg3"""
    return f"postgresql+psycopg://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"


def create_sqlalchemy_engine() -> Engine:
    conn_string: str = ""
    conn = None
    try:
        # Cria engine do SQLAlchemy usando psycopg3
        conn_string = get_sqlalchemy_connection_string()
        engine = create_engine(conn_string, echo=False)
        return engine
    except Exception as e:
        if conn_string:
            print(
                f"Erro inesperado tentando abrir conexão com conn_string = {conn_string}. "
                + f"Error: {e}"
            )
            raise PmRagError(
                f"⚠️ **Erro:** Erro na conn_string '{conn_string}'. "
                + "Certifique-se de que os requisitos foram atendidos",
                error_code=1003,
            )


def exec_query(command_id) -> DataFrame:  # pd.DataFrame:
    cmd = SQL_COMMANDS[command_id]
    clean_sql = cmd.strip()
    extract_tag = False
    if command_id in ENHANCEDS:
        extract_tag = True

    column_names: list[str]
    engine: Engine = create_sqlalchemy_engine()
    conn = engine.connect()
    try:
        result: CursorResult[Any] = conn.execute(text(clean_sql))
        column_names = list(result.keys())
        last_column = column_names[-1]
        new_column_name: str = f"{last_column}_len"
        rows: Sequence[Row[tuple[object, ...]]] = result.fetchall()
        df = pd.DataFrame(data=rows, columns=column_names)
        if extract_tag:
            # Cria a nova coluna no DataFrame
            #    - Acessa a coluna de strings (last_column)
            #    - Usa o acessador .str para operações de string
            #    - Aplica .len() para obter o tamanho da string
            df[new_column_name] = df[last_column].str.len()

        # print(df)
        return df
    except:
        raise PmRagError(
            f"⚠️ **Erro: Erro ao executar o comando '{clean_sql}'. "
            + "Verifique, por favor ",
            error_code=1005,
        )


def exec_os_command(comando: list[str]) -> tuple[str, str]:
    """
    Executa um comando do sistema operacional e retorna uma string formatada
    contendo o comando, o código de retorno, a saída padrão (stdout) e a
    saída de erro (stderr).

    :param comando: Uma lista de strings representando o comando e seus argumentos.
    :return: Uma tuple de string, string contendo o resultado de STDOUT e STDERR.
    """
    try:
        # Executa o comando e captura o resultado
        # capture_output=True: Captura a saída (stdout e stderr)
        # text=True: Retorna a saída como string (em vez de bytes)
        # check=False: Não levanta exceção se o código de retorno for diferente de zero
        resultado = subprocess.run(comando, capture_output=True, text=True, check=False)

        # Formata a string de saída
        std_out = f"Comando: {' '.join(comando)}\n"
        std_out += f"Status de Retorno (Exit Code): {resultado.returncode}\n\n"
        std_out += "--- SAÍDA PADRÃO (STDOUT) ---\n"
        std_out += resultado.stdout
        std_err = "\n--- SAÍDA DE ERRO (STDERR) ---\n"
        std_err += resultado.stderr

        return (std_out, std_err)

    except FileNotFoundError:
        raise PmRagError(
            f"⚠️ **Erro:** O comando '{comando[0]}' não foi encontrado. "
            + "Certifique-se de que ele está no seu PATH.",
            error_code=1002,
        )
    except Exception as e:
        raise PmRagError(
            f"⚠️ **Erro Inesperado durante a execução:** {e} ",
            error_code=1001,
        )
        return f"⚠️ "


@final
class PmRagError(Exception):
    def __init__(self, message, **kwargs):
        # Armazena argumentos adicionais no dicionário da instância
        self.__dict__.update(kwargs)

        # CHAME o construtor da classe base (Exception) PASSANDO APENAS a mensagem
        # A forma correta é:
        super().__init__(message)

        # Opcional: Armazenar a mensagem como atributo próprio
        self.message = message

    @override
    def __str__(self):
        """
        Retorna a representação em string da exceção, que é a mensagem de erro.
        """
        # A mensagem é o primeiro (e geralmente único) elemento em self.args
        return self.message

    @override
    def __repr__(self):
        """
        Retorna a representação "oficial" do objeto (adequada para debug e logs).
        Inclui a mensagem e todos os kwargs adicionais.
        """
        # Inicia com o nome da classe e a mensagem (repr)
        repr_string = f"{self.__class__.__name__}({repr(self.message)}"

        # Adiciona os kwargs que estão no __dict__ (exceto a 'message' já tratada)
        extra_args = []
        for key, value in self.__dict__.items():
            # Ignora atributos internos e a própria mensagem, que já foi adicionada
            if not key.startswith("_") and key != "message":
                extra_args.append(f"{key}={repr(value)}")

        # Se houver argumentos extras, adiciona-os à string
        if extra_args:
            repr_string += ", " + ", ".join(extra_args)

        repr_string += ")"
        return repr_string


def test_similarity_search():
    """Testa uma busca de similaridade usando pgvector"""
    print("\n" + "=" * 80)
    print("ETAPA 4: TESTANDO BUSCA DE SIMILARIDADE")
    print("=" * 80)

    conn = None
    cur = None

    try:
        # Cria conexão
        conn = create_psycopg_connection()
        cur = conn.cursor()

        # Gera um vetor aleatório de 512 dimensões para teste
        print("\n🔍 Gerando vetor de busca aleatório (512 dimensões)...")
        random_vector = np.random.rand(512).tolist()

        # Busca os 5 registros mais similares usando distância de cosseno
        print("🔍 Executando busca por similaridade (top 5)...\n")

        query = """
            SELECT sap_order_id, equipment_number, order_type,
                   LEFT(maintenance_text, 120) as preview,
                   embedding <=> %s::vector as distance
            FROM sap_pm_rag_data
            ORDER BY distance
            LIMIT 5;
        """

        cur.execute(query, (random_vector,))
        results = cur.fetchall()

        print("📊 Resultados da busca (ordenados por similaridade):")
        print("-" * 80)
        for idx, (order_id, equipment, order_type, preview, distance) in enumerate(
            results, 1
        ):
            print(
                f"\n{idx}. Ordem: {order_id} | Tipo: {order_type} | Equipamento: {equipment}"
            )
            print(f"   Distância: {distance:.6f}")
            print(f"   Preview: {preview}...")

        print("\n" + "=" * 80)
        print("✓ TESTE DE SIMILARIDADE CONCLUÍDO!")
        print("=" * 80)

    except Exception as e:
        print(f"\n❌ ERRO no teste de similaridade: {e}")
        import traceback

        traceback.print_exc()
        raise

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()



def main():
    """
    Função usada apenas para teste rápido de funções definidas neste script Python
    """
    from pm_rag.util import exec_os_command, exec_query, test_similarity_search

    # Verificar se PostgreSQL está rodando
    command = ["pg_isready", "-h", str(DB_CONFIG['host']), "-p", str(DB_CONFIG['port'])]
    std_out, stderr = exec_os_command(command)
    print(f"{std_out}{stderr}")

    df = exec_query("get_maintenance_text")
    print(df)
    print("+" * 80)
    df = exec_query("get_distinct_order_type")
    print(df)
    print("+" * 80)
    df = exec_query("equipment_maintainance_priority")
    print(df)

    test_similarity_search()

if __name__ == "__main__":
    main()
