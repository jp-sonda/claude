#!/usr/bin/env python3
"""
Exemplo de uso da análise de dependências de tabelas.

Este script demonstra como usar as classes TableDependencyGraph e
DatabaseBatchOperations para analisar dependências e gerar comandos em lote.
"""

import json
import os
from pathlib import Path
from psql_catalog.dependency_graph import TableDependencyGraph, analyze_schema_file
from psql_catalog.batch_operations import DatabaseBatchOperations


def create_sample_schema_file():
    """Cria um arquivo de exemplo do schema JSON para demonstração."""
    sample_schema = {
        "command": "describe-all",
        "timestamp": "2025-08-24T10:30:00",
        "database": "ecommerce_db",
        "schema": "public",
        "tables": {
            "users": {
                "columns": [
                    {"column_name": "id", "data_type": "integer", "is_nullable": "NO"},
                    {"column_name": "name", "data_type": "character varying", "is_nullable": "NO"},
                    {"column_name": "email", "data_type": "character varying", "is_nullable": "YES"}
                ],
                "indexes": [
                    {"index_name": "users_pkey", "column_name": "id", "is_unique": True, "is_primary": True}
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
                    {"column_name": "id", "data_type": "integer", "is_nullable": "NO"},
                    {"column_name": "name", "data_type": "character varying", "is_nullable": "NO"},
                    {"column_name": "parent_id", "data_type": "integer", "is_nullable": "YES"}
                ],
                "indexes": [
                    {"index_name": "categories_pkey", "column_name": "id", "is_unique": True, "is_primary": True}
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
                    {"column_name": "id", "data_type": "integer", "is_nullable": "NO"},
                    {"column_name": "name", "data_type": "character varying", "is_nullable": "NO"},
                    {"column_name": "price", "data_type": "numeric", "is_nullable": "YES"},
                    {"column_name": "category_id", "data_type": "integer", "is_nullable": "YES"}
                ],
                "indexes": [
                    {"index_name": "products_pkey", "column_name": "id", "is_unique": True, "is_primary": True}
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
                    {"column_name": "id", "data_type": "integer", "is_nullable": "NO"},
                    {"column_name": "user_id", "data_type": "integer", "is_nullable": "NO"},
                    {"column_name": "total", "data_type": "numeric", "is_nullable": "YES"},
                    {"column_name": "order_date", "data_type": "timestamp", "is_nullable": "NO"}
                ],
                "indexes": [
                    {"index_name": "orders_pkey", "column_name": "id", "is_unique": True, "is_primary": True}
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
                    {"column_name": "id", "data_type": "integer", "is_nullable": "NO"},
                    {"column_name": "order_id", "data_type": "integer", "is_nullable": "NO"},
                    {"column_name": "product_id", "data_type": "integer", "is_nullable": "NO"},
                    {"column_name": "quantity", "data_type": "integer", "is_nullable": "NO"},
                    {"column_name": "price", "data_type": "numeric", "is_nullable": "NO"}
                ],
                "indexes": [
                    {"index_name": "order_items_pkey", "column_name": "id", "is_unique": True, "is_primary": True}
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

    # Salvar arquivo de exemplo
    sample_file = "sample_schema.json"
    with open(sample_file, 'w', encoding='utf-8') as f:
        json.dump(sample_schema, f, indent=2)

    print(f"✓ Arquivo de exemplo criado: {sample_file}")
    return sample_file


def demonstrate_basic_usage():
    """Demonstra o uso básico da análise de dependências."""
    print("=" * 60)
    print("DEMONSTRAÇÃO: Análise Básica de Dependências")
    print("=" * 60)

    # Criar arquivo de exemplo
    schema_file = create_sample_schema_file()

    try:
        # Carregar e analisar o schema
        print("\n1. Carregando e analisando o schema...")
        graph = TableDependencyGraph()
        graph.load_from_json_file(schema_file)

        # Mostrar resumo do grafo
        print("\n2. Resumo do grafo de dependências:")
        graph.print_graph_summary()

        # Mostrar dependências detalhadas
        print("\n3. Dependências detalhadas:")
        graph.print_detailed_dependencies()

        # Obter ordens de operação
        print("\n4. Ordens recomendadas para operações:")
        insert_order = graph.get_insert_order()
        drop_order = graph.get_drop_order()

        print(f"\n   Para INSERT (dependências primeiro):")
        for i, table in enumerate(insert_order, 1):
            deps = graph.get_dependencies(table)
            deps_str = f" (depende de: {', '.join(sorted(deps))})" if deps else " (sem dependências)"
            print(f"     {i}. {table}{deps_str}")

        print(f"\n   Para DROP (dependentes primeiro):")
        for i, table in enumerate(drop_order, 1):
            dependents = graph.get_dependents(table)
            deps_str = f" (dependido por: {', '.join(sorted(dependents))})" if dependents else " (sem dependentes)"
            print(f"     {i}. {table}{deps_str}")

        return schema_file

    except Exception as e:
        print(f"Erro na demonstração básica: {e}")
        return None


def demonstrate_batch_operations(schema_file):
    """Demonstra o uso das operações em lote."""
    print("\n" + "=" * 60)
    print("DEMONSTRAÇÃO: Operações em Lote")
    print("=" * 60)

    try:
        # Criar handler de operações em lote
        batch_ops = DatabaseBatchOperations(schema_file)

        # Demonstrar diferentes tipos de comandos
        print("\n1. Comandos DROP (com CASCADE):")
        drop_statements = batch_ops.generate_drop_statements(cascade=True)
        for i, stmt in enumerate(drop_statements, 1):
            print(f"   {i}. {stmt}")

        print("\n2. Comandos TRUNCATE (com RESTART IDENTITY e CASCADE):")
        truncate_statements = batch_ops.generate_truncate_statements(
            cascade=True,
            restart_identity=True
        )
        for i, stmt in enumerate(truncate_statements, 1):
            print(f"   {i}. {stmt}")

        print("\n3. Templates INSERT (com nomes das colunas):")
        insert_templates = batch_ops.generate_insert_template_statements()
        for i, stmt in enumerate(insert_templates, 1):
            print(f"   {i}. {stmt}")

        # Salvar scripts SQL
        print("\n4. Salvando scripts SQL:")

        # Salvar DROP script
        drop_file = "drop_tables.sql"
        batch_ops.save_sql_script('drop', drop_file, cascade=True)
        print(f"   ✓ DROP script salvo em: {drop_file}")

        # Salvar TRUNCATE script
        truncate_file = "truncate_tables.sql"
        batch_ops.save_sql_script('truncate', truncate_file, cascade=True, restart_identity=True)
        print(f"   ✓ TRUNCATE script salvo em: {truncate_file}")

        # Salvar INSERT templates
        insert_file = "insert_templates.sql"
        batch_ops.save_sql_script('insert_template', insert_file)
        print(f"   ✓ INSERT templates salvos em: {insert_file}")

        return [drop_file, truncate_file, insert_file]

    except Exception as e:
        print(f"Erro na demonstração de operações em lote: {e}")
        return []


def demonstrate_convenience_functions(schema_file):
    """Demonstra o uso das funções de conveniência."""
    print("\n" + "=" * 60)
    print("DEMONSTRAÇÃO: Funções de Conveniência")
    print("=" * 60)

    try:
        # Usar funções de conveniência
        print("\n1. Usando funções simples para obter ordens:")

        from psql_catalog.dependency_graph import get_table_insert_order, get_table_drop_order

        insert_order = get_table_insert_order(schema_file)
        drop_order = get_table_drop_order(schema_file)

        print(f"   INSERT order: {' -> '.join(insert_order)}")
        print(f"   DROP order:   {' -> '.join(drop_order)}")

        print("\n2. Análise completa usando função de conveniência:")
        from psql_catalog.dependency_graph import print_dependency_analysis

        print_dependency_analysis(schema_file)

    except Exception as e:
        print(f"Erro na demonstração de funções de conveniência: {e}")


def demonstrate_practical_usage():
    """Demonstra casos de uso práticos."""
    print("\n" + "=" * 60)
    print("DEMONSTRAÇÃO: Casos de Uso Práticos")
    print("=" * 60)

    schema_file = "sample_schema.json"

    print("\n1. CASO DE USO: Preparar ambiente de teste")
    print("   Cenário: Limpar todas as tabelas e recarregar dados de teste")

    try:
        graph = analyze_schema_file(schema_file)

        # Passo 1: Desabilitar constraints
        print("\n   Passo 1: Gerar comandos para desabilitar constraints")
        batch_ops = DatabaseBatchOperations(schema_file)
        disable_fk = batch_ops.generate_disable_constraints_statements()
        for stmt in disable_fk[:2]:  # Mostrar apenas os primeiros 2
            print(f"     {stmt}")
        print(f"     ... (total: {len(disable_fk)} comandos)")

        # Passo 2: Truncate em ordem segura
        print("\n   Passo 2: TRUNCATE em ordem segura")
        truncate_order = graph.get_drop_order()  # Mesma ordem do DROP
        for i, table in enumerate(truncate_order, 1):
            print(f"     {i}. TRUNCATE TABLE {table} RESTART IDENTITY;")

        # Passo 3: Reabilitar constraints
        print("\n   Passo 3: Gerar comandos para reabilitar constraints")
        enable_fk = batch_ops.generate_enable_constraints_statements()
        for stmt in enable_fk[:2]:  # Mostrar apenas os primeiros 2
            print(f"     {stmt}")
        print(f"     ... (total: {len(enable_fk)} comandos)")

        # Passo 4: INSERT em ordem segura
        print("\n   Passo 4: INSERT dados de teste em ordem segura")
        insert_order = graph.get_insert_order()
        for i, table in enumerate(insert_order, 1):
            print(f"     {i}. Inserir dados em {table}")

    except Exception as e:
        print(f"   Erro: {e}")

    print("\n2. CASO DE USO: Backup e restore")
    print("   Cenário: Fazer backup dos dados respeitando dependências")

    try:
        # Para backup: ordem INSERT (dependências primeiro)
        insert_order = get_table_insert_order(schema_file)
        print(f"\n   Ordem para BACKUP (pg_dump): {' -> '.join(insert_order)}")

        # Para restore: mesma ordem
        print(f"   Ordem para RESTORE: {' -> '.join(insert_order)}")

    except Exception as e:
        print(f"   Erro: {e}")

    print("\n3. CASO DE USO: Migração de schema")
    print("   Cenário: Dropar e recriar todas as tabelas")

    try:
        drop_order = get_table_drop_order(schema_file)
        insert_order = get_table_insert_order(schema_file)

        print(f"\n   1. DROP em ordem segura: {' -> '.join(drop_order)}")
        print(f"   2. CREATE em ordem segura: {' -> '.join(insert_order)}")

    except Exception as e:
        print(f"   Erro: {e}")


def cleanup_demo_files():
    """Limpa os arquivos gerados na demonstração."""
    demo_files = [
        "sample_schema.json",
        "drop_tables.sql",
        "truncate_tables.sql",
        "insert_templates.sql"
    ]

    print("\n" + "=" * 60)
    print("LIMPEZA: Removendo arquivos de demonstração")
    print("=" * 60)

    for file in demo_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"✓ Removido: {file}")
        else:
            print(f"- Não encontrado: {file}")


def main():
    """Função principal - executa todas as demonstrações."""
    print("PSQL-CATALOG: Demonstração de Análise de Dependências")
    print("=" * 80)
    print()
    print("Esta demonstração mostra como usar as classes TableDependencyGraph")
    print("e DatabaseBatchOperations para analisar dependências entre tabelas")
    print("e gerar comandos SQL em lote na ordem correta.")
    print()

    try:
        # Demonstrações
        schema_file = demonstrate_basic_usage()
        if schema_file:
            demonstrate_batch_operations(schema_file)
            demonstrate_convenience_functions(schema_file)
            demonstrate_practical_usage()

        print("\n" + "=" * 80)
        print("✓ DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 80)

        # Perguntar se deve limpar os arquivos
        response = input("\nDeseja remover os arquivos de demonstração? (s/N): ").lower().strip()
        if response in ('s', 'sim', 'y', 'yes'):
            cleanup_demo_files()
        else:
            print("\nArquivos de demonstração mantidos para sua análise:")
            print("- sample_schema.json")
            print("- drop_tables.sql")
            print("- truncate_tables.sql")
            print("- insert_templates.sql")

    except KeyboardInterrupt:
        print("\n\nDemonstração interrompida pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro durante a demonstração: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
