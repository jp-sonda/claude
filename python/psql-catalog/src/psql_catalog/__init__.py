"""
psql-catalog: A PostgreSQL catalog navigator for database schemas

A comprehensive tool for exploring PostgreSQL database structures,
including schemas, tables, columns, indexes, and integrity constraints.
"""

__version__ = "0.1.0"
__author__ = "Seu Nome"
__email__ = "seu.email@exemplo.com"

from psql_catalog.catalog import PostgreSQLCatalog
from psql_catalog.display import display_table, display_constraints, display_database_info
from psql_catalog.exceptions import (
    PSQLCatalogError,
    DatabaseConnectionError,
    QueryExecutionError,
    TableNotFoundError,
    SchemaNotFoundError,
    InvalidConnectionStringError
)
from psql_catalog.main import main

__all__ = [
    "PostgreSQLCatalog",
    "display_table",
    "display_constraints",
    "display_database_info",
    "PSQLCatalogError",
    "DatabaseConnectionError",
    "QueryExecutionError",
    "TableNotFoundError",
    "SchemaNotFoundError",
    "InvalidConnectionStringError",
    "main"
]
