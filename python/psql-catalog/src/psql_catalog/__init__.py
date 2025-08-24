"""
psql-catalog: A PostgreSQL catalog navigator for database schemas

A comprehensive tool for exploring PostgreSQL database structures,
including schemas, tables, columns, indexes, and integrity constraints.
Supports both rich formatted output and JSON serialization.
"""

__version__ = "0.6.0"
__author__ = "Seu Nome"
__email__ = "seu.email@exemplo.com"

from .catalog import PostgreSQLCatalog
from .display import display_table, display_constraints, display_database_info, display_json
from .serialization import (
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
from .exceptions import (
    PSQLCatalogError,
    DatabaseConnectionError,
    QueryExecutionError,
    TableNotFoundError,
    SchemaNotFoundError,
    InvalidConnectionStringError
)
from .main import main

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
    "main"
]
