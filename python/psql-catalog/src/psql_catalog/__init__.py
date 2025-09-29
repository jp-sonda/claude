"""
psql-catalog: A PostgreSQL catalog navigator for database schemas

A comprehensive tool for exploring PostgreSQL database structures,
including schemas, tables, columns, indexes, and integrity constraints.
Supports both rich formatted output and JSON serialization.
"""

__version__ = "0.7.1"
__author__ = "Seu Nome"
__email__ = "seu.email@exemplo.com"

from psql_catalog.catalog import PostgreSQLCatalog
from psql_catalog.display import display_table, display_constraints, display_database_info, display_json
from psql_catalog.serialization import (
    JSONSerializableMixin,
    CatalogResult,
    SchemasResult,
    TablesResult,
    DescribeResult,
    QueryResult,
    InfoResult,
    create_schemas_result,
    create_tables_result,
    create_describe_result,
    create_query_result,
    create_info_result,
    output_json,
    save_json_to_file
)
from psql_catalog.exceptions import (
    PSQLCatalogError,
    DatabaseConnectionError,
    QueryExecutionError,
    TableNotFoundError,
    SchemaNotFoundError,
    InvalidConnectionStringError
)
from psql_catalog.main import main
from psql_catalog.dependency_graph import (
    TableDependencyGraph,
    TableDependency,
    TableNode,
    CycleDetectionError,
    GraphTraversalOrder,
    analyze_schema_file,
    get_table_insert_order,
    get_table_drop_order,
    print_dependency_analysis
)
from psql_catalog.batch_operations import (
    DatabaseBatchOperations,
    BatchOperationError
)

__all__ = [
    "PostgreSQLCatalog",
    "display_table",
    "display_constraints",
    "display_database_info",
    "display_json",
    "JSONSerializableMixin",
    "CatalogResult",
    "SchemasResult",
    "TablesResult",
    "DescribeResult",
    "QueryResult",
    "InfoResult",
    "create_schemas_result",
    "create_tables_result",
    "create_describe_result",
    "create_query_result",
    "create_info_result",
    "output_json",
    "save_json_to_file",
    "PSQLCatalogError",
    "DatabaseConnectionError",
    "QueryExecutionError",
    "TableNotFoundError",
    "SchemaNotFoundError",
    "InvalidConnectionStringError",
    "main",
    # Dependency analysis classes
    "TableDependencyGraph",
    "TableDependency",
    "TableNode",
    "CycleDetectionError",
    "GraphTraversalOrder",
    "analyze_schema_file",
    "get_table_insert_order",
    "get_table_drop_order",
    "print_dependency_analysis",
    # Batch operations classes
    "DatabaseBatchOperations",
    "BatchOperationError"
]
