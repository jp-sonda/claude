"""
Custom exceptions for psql-catalog.
"""


class PSQLCatalogError(Exception):
    """Base exception class for psql-catalog."""
    pass


class DatabaseConnectionError(PSQLCatalogError):
    """Raised when database connection fails."""
    pass


class QueryExecutionError(PSQLCatalogError):
    """Raised when query execution fails."""
    pass


class TableNotFoundError(PSQLCatalogError):
    """Raised when a requested table is not found."""
    pass


class SchemaNotFoundError(PSQLCatalogError):
    """Raised when a requested schema is not found."""
    pass


class InvalidConnectionStringError(PSQLCatalogError):
    """Raised when connection string format is invalid."""
    pass
