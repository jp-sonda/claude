#!/usr/bin/env python3
"""
Script para executar a criação da tabela, função e inserção de dados
Importa as definições SQL do arquivo ddl_01.py
Utiliza: numpy, pgvector, psycopg[binary] e SQLAlchemy
"""

import sys
from pathlib import Path
import time
import psycopg
from pgvector.psycopg import register_vector
from sqlalchemy import Engine, create_engine, text
import numpy as np

from pm_rag.util import create_psycopg_connection, get_sqlalchemy_connection_string

# Adiciona o diretório ao path para importar o módulo ddl_01
sys.path.insert(0, str(Path(__file__).parent))

# Importa as definições SQL do arquivo ddl_01.py
from .ddl_01 import (
    sap_pm_rag_data_table,
    generate_random_embedding_function,
    insert_simulated_data,
)


def create_table_and_function():
    """
    Passo 1: Cria a tabela sap_pm_rag_data
    Passo 2: Cria a função generate_random_embedding
    Utiliza psycopg para executar os comandos DDL
    """
    print("\n" + "=" * 80)
    print("ETAPA 1: CRIANDO TABELA E FUNÇÃO")
    print("=" * 80)

    conn = None
    cur = None

    try:
        # Cria conexão
        conn = create_psycopg_connection()
        cur = conn.cursor()

        # Habilita a extensão pgvector
        print("\n[1/4] Habilitando extensão pgvector...")
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        print("✓ Extensão pgvector habilitada")

        # Remove tabela se existir (para permitir re-execução)
        print("\n[2/4] Removendo tabela existente (se houver)...")
        cur.execute("DROP TABLE IF EXISTS sap_pm_rag_data CASCADE;")
        print("✓ Tabela anterior removida (se existia)")

        # Passo 1: Cria a tabela
        print("\n[3/4] Criando tabela sap_pm_rag_data...")
        cur.execute(sap_pm_rag_data_table)
        print("✓ Tabela criada com sucesso")

        # Passo 2: Cria a função
        print("\n[4/4] Criando função generate_random_embedding...")
        cur.execute(generate_random_embedding_function)
        print("✓ Função criada com sucesso")

        # Commit das alterações DDL
        conn.commit()
        print("\n" + "=" * 80)
        print("✓ TABELA E FUNÇÃO CRIADAS COM SUCESSO!")
        print("=" * 80)

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"\n❌ ERRO ao criar tabela/função: {e}")
        raise

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def execute_inserts():
    """
    Passo 3: Itera sobre insert_simulated_data e executa um a um
    Passo 4: Faz commit da transação
    Utiliza SQLAlchemy para executar os INSERTs
    """
    print("\n" + "=" * 80)
    print("ETAPA 2: EXECUTANDO INSERTS")
    print("=" * 80)

    engine = None
    conn = None

    try:
        # Cria engine do SQLAlchemy usando psycopg3
        conn_string = get_sqlalchemy_connection_string()
        engine = create_engine(conn_string, echo=False)

        total_inserts = len(insert_simulated_data)
        success_count = 0
        error_count = 0
        skipped_count = 0
        insert_count = 1

        print(f"\n📊 Total de comandos na lista: {total_inserts}")
        print("🔄 Iniciando inserção...\n")

        start_time = time.time()

        # Passo 3: Itera sobre a lista insert_simulated_data
        conn = engine.connect()

        try:
            for idx, insert_sql in enumerate(insert_simulated_data, 1):
                try:
                    # Limpa o SQL (remove espaços em branco desnecessários)
                    clean_sql = insert_sql.strip()

                    # Pula linhas vazias ou apenas com comentários
                    if not clean_sql or clean_sql.startswith("--"):
                        skipped_count += 1
                        continue

                    # Detecta se é SELECT
                    if clean_sql.upper().startswith("SELECT"):
                        # Executa SELECT e exibe resultado
                        result = conn.execute(text(clean_sql))
                        row = result.fetchone()
                        if row:
                            # Exibe apenas os valores, sem cabeçalho
                            print(f"📄{' | '.join(str(v) for v in row)}")
                        continue

                    # Executa o INSERT um a um
                    print(f"Executando o {insert_count}º comando insert")
                    result = conn.execute(text(clean_sql))

                    # Passo 4: Faz commit após cada insert
                    conn.commit()

                    success_count += 1
                    insert_count += 1

                    # Mostra progresso a cada 5 inserts
                    # if success_count % 5 == 0:
                    print(f"  ✓ [{success_count} inserts executados...].")

                except Exception as e:
                    error_count += 1
                    print(f"\n❌ ERRO no comando {idx}:")
                    print(f"Message: {str(e)}")
                    print(f"   SQL: {clean_sql[:5000]}...")
                    print(f"   Erro: {str(e)[:150]}...")
                    # Continua executando os próximos mesmo com erro
                    continue

            end_time = time.time()
            elapsed = end_time - start_time

            # Resumo da execução
            print("\n" + "=" * 80)
            print("RESULTADO DA INSERÇÃO")
            print("=" * 80)
            print(f"✓ Inserts bem-sucedidos: {success_count}")
            print(f"⊘ Comandos pulados (vazios/comentários): {skipped_count}")
            print(f"❌ Inserts com erro: {error_count}")
            print(f"⏱️  Tempo total: {elapsed:.2f} segundos")

            if success_count > 0:
                print(f"⚡ Taxa: {success_count / elapsed:.2f} inserts/segundo")

            print("=" * 80)

        finally:
            if conn:
                conn.close()

    except Exception as e:
        print(f"\n❌ ERRO GERAL durante inserts: {e}")
        raise

    finally:
        if engine:
            engine.dispose()


def verify_data():
    """Verifica os dados inseridos no banco"""
    print("\n" + "=" * 80)
    print("ETAPA 3: VERIFICANDO DADOS INSERIDOS")
    print("=" * 80)

    engine = None
    conn = None

    try:
        conn_string = get_sqlalchemy_connection_string()
        engine: Engine = create_engine(conn_string, echo=False)
        conn = engine.connect()

        try:
            # Conta total de registros
            result = conn.execute(text("SELECT COUNT(*) FROM sap_pm_rag_data;"))
            total_records = result.scalar()
            print(f"\n📊 Total de registros na tabela: {total_records}")

            # Conta por tipo de ordem
            result = conn.execute(
                text(
                    """
                SELECT order_type, COUNT(*) as count
                FROM sap_pm_rag_data
                GROUP BY order_type
                ORDER BY order_type;
            """
                )
            )
            print("\n📋 Distribuição por tipo de ordem:")
            for row in result:
                print(f"   • {row[0]}: {row[1]} registros")

            # Conta registros por chunk_id
            result = conn.execute(
                text(
                    """
                SELECT chunk_id, COUNT(*) as count
                FROM sap_pm_rag_data
                GROUP BY chunk_id
                ORDER BY chunk_id;
            """
                )
            )
            print("\n📦 Distribuição por chunk:")
            for row in result:
                print(f"   • Chunk {row[0]}: {row[1]} registros")

            # Equipamentos com mais registros
            result = conn.execute(
                text(
                    """
                SELECT equipment_number, COUNT(*) as count
                FROM sap_pm_rag_data
                GROUP BY equipment_number
                ORDER BY count DESC
                LIMIT 10;
            """
                )
            )
            print("\n🔧 Top 10 equipamentos com mais registros:")
            for row in result:
                print(f"   • {row[0]}: {row[1]} registros")

            # Verifica dimensão dos embeddings
            result = conn.execute(
                text(
                    """
                SELECT vector_dims(embedding) as dims
                FROM sap_pm_rag_data
                LIMIT 1;
            """
                )
            )
            dims = result.scalar()
            print(f"\n🔢 Dimensão dos vetores de embedding: {dims}")

            # Mostra alguns exemplos de registros
            result = conn.execute(
                text(
                    """
                SELECT sap_order_id, functional_location, equipment_number,
                       order_type, LEFT(maintenance_text, 100) as text_preview
                FROM sap_pm_rag_data
                ORDER BY id
                LIMIT 3;
            """
                )
            )
            print("\n📄 Exemplo dos primeiros 3 registros:")
            for idx, row in enumerate(result, 1):
                print(f"\n   {idx}. Ordem: {row[0]} | Tipo: {row[3]}")
                print(f"      Local: {row[1]}")
                print(f"      Equipamento: {row[2]}")
                print(f"      Texto: {row[4]}...")

            print("\n" + "=" * 80)
            print("✓ VERIFICAÇÃO CONCLUÍDA!")
            print("=" * 80)

        finally:
            if conn:
                conn.close()

    except Exception as e:
        print(f"\n❌ ERRO na verificação: {e}")
        raise

    finally:
        if engine:
            engine.dispose()


def main():
    """Função principal que orquestra todas as etapas"""
    print("\n" + "#" * 80)
    print("#" + " " * 78 + "#")
    print("#" + "  SCRIPT DE CRIAÇÃO E POPULAÇÃO - SAP PM RAG DATA".center(78) + "#")
    print("#" + " " * 78 + "#")
    print("#" * 80)
    print("\n📦 Pacotes utilizados: numpy, pgvector, psycopg[binary], SQLAlchemy")
    print(f"📁 Importando dados de: {Path(__file__).parent / 'ddl_01.py'}")
    print(
        f"🗄️  Banco de dados: {DB_CONFIG['dbname']} @ {DB_CONFIG['host']}:{DB_CONFIG['port']}"
    )

    try:
        # Etapa 1: Criar tabela e função
        create_table_and_function()

        # Etapa 2: Executar inserts (iterar e fazer commit)
        execute_inserts()

        # Etapa 3: Verificar dados inseridos
        verify_data()

        # Etapa 4: Testar busca de similaridade
        test_similarity_search()

        # Sucesso!
        print("\n" + "#" * 80)
        print("#" + " " * 78 + "#")
        print("#" + "  ✅ SCRIPT EXECUTADO COM SUCESSO!".center(78) + "#")
        print("#" + " " * 78 + "#")
        print("#" * 80 + "\n")

        return 0

    except Exception as e:
        # Erro na execução
        print("\n" + "#" * 80)
        print("#" + " " * 78 + "#")
        print("#" + "  ❌ ERRO NA EXECUÇÃO DO SCRIPT".center(78) + "#")
        print("#" + " " * 78 + "#")
        print("#" * 80)
        print(f"\n💥 Erro: {e}\n")

        # Mostra traceback completo
        import traceback

        traceback.print_exc()

        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
