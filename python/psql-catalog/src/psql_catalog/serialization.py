"""
JSON serialization utilities for psql-catalog.
"""

import json
from typing import Self, Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass, field, asdict

class JSONSerializableMixin:
    """Mixin class for JSON serialization support."""

    @classmethod
    def from_json(cls, json_string: str) -> Self:
        """Create instance from JSON string."""
        return cls(**json.loads(json_string))

    def as_json(self, indent: Optional[int] = None) -> str:
        """Convert instance to JSON string."""
        # Deve suportar objetos aninhados
        # return json.dumps(vars(self), indent=indent, default=self._json_serializer)
        # TODO: CUIDADO type: ignore abaixo vale apenas para situações em que o Mixin está aplicado a dataclass.
        return json.dumps(asdict(self), indent=indent, default=self._json_serializer) # type: ignore

    @staticmethod
    def _json_serializer(obj):
        """Custom JSON serializer for special types."""
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


@dataclass
class CatalogResult(JSONSerializableMixin):
    """Base class for catalog query results."""

    command: str
    timestamp: datetime
    database: str
    schema: Optional[str] = None
    table: Optional[str] = None

    def __post_init__(self):
        if isinstance(self.timestamp, str):
            self.timestamp = datetime.fromisoformat(self.timestamp)


@dataclass
class SchemasResult(CatalogResult):
    """Result for schemas command."""

    schemas: List[Dict[str, Any]] = field(default_factory=list)

    def __post_init__(self):
        super().__post_init__()
        self.command = "schemas"


@dataclass
class TablesResult(CatalogResult):
    """Result for tables command."""

    tables: List[Dict[str, Any]] = field(default_factory=list)

    def __post_init__(self):
        super().__post_init__()
        self.command = "tables"



@dataclass
class TableStructure(JSONSerializableMixin):
    """Structure information for a table."""

    columns: List[Dict[str, Any]] = field(default_factory=list)
    indexes: List[Dict[str, Any]] = field(default_factory=list)
    constraints: Optional[List[Dict[str, Any]]] = None
    foreign_key_details: Optional[List[Dict[str, Any]]] = None

    @classmethod
    def null(cls):
        """Returns a singleton Null Object for this class."""
        # Cria uma instância da classe NullTableStructure
        # return NullTableStructure()

        """Returns a Null Object for this class by direct instantiation."""
        return cls() # cls([], [], None, None)

@dataclass
class NullTableStructure(TableStructure):
    """A Null Object for TableStructure."""
    columns: List[Dict[str, Any]] = field(default_factory=list)
    indexes: List[Dict[str, Any]] = field(default_factory=list)
    constraints: Optional[List[Dict[str, Any]]] = field(default_factory=list)
    foreign_key_details: Optional[List[Dict[str, Any]]] = field(default_factory=list)

@dataclass
class DescribeResult(CatalogResult):
    """Result for describe command."""

    # Exemplo de uso
    # my_structure = TableStructure(...)
    # result = DescribeResult(structure=my_structure)
    # ou
    # result = DescribeResult(structure=my_structure, show_constraints=True)

    structure: TableStructure = field(default_factory=TableStructure)
    show_constraints: bool = False

    def __post_init__(self):
        super().__post_init__()
        self.command = "describe"


@dataclass
class QueryResult(CatalogResult):
    """Result for query command."""

    sql: str = ''
    results: List[Dict[str, Any]] = field(default_factory=list)
    row_count: int = 0

    def __post_init__(self):
        super().__post_init__()
        self.command = "query"
        if not hasattr(self, 'row_count'):
            self.row_count = len(self.results)


@dataclass
class DatabaseInfo(JSONSerializableMixin):
    """Database connection information."""

    database_name: str = ''
    current_user: str = ''
    version: str = ''
    encoding: str = ''
    timezone: str = ''
    timestamp: Optional[datetime] = None


@dataclass
class InfoResult(CatalogResult):
    """Result for info command."""

    info: DatabaseInfo= field(default_factory=DatabaseInfo)

    def __post_init__(self):
        super().__post_init__()
        self.command = "info"


def create_schemas_result(schemas: List[Dict[str, Any]], database: str) -> SchemasResult:
    """Create a SchemasResult instance."""
    return SchemasResult(
        command="schemas",
        timestamp=datetime.now(),
        database=database,
        schemas=schemas
    )


def create_tables_result(tables: List[Dict[str, Any]], database: str, schema: str) -> TablesResult:
    """Create a TablesResult instance."""
    return TablesResult(
        command="tables",
        timestamp=datetime.now(),
        database=database,
        schema=schema,
        tables=tables
    )


def create_describe_result(
    columns: List[Dict[str, Any]],
    indexes: List[Dict[str, Any]],
    database: str,
    schema: str,
    table: str,
    show_constraints: bool = False,
    constraints: Optional[List[Dict[str, Any]]] = None,
    foreign_key_details: Optional[List[Dict[str, Any]]] = None
) -> DescribeResult:
    """Create a DescribeResult instance."""
    structure = TableStructure(
        columns=columns,
        indexes=indexes,
        constraints=constraints if show_constraints else None,
        foreign_key_details=foreign_key_details if show_constraints else None
    )

    return DescribeResult(
        command="describe",
        timestamp=datetime.now(),
        database=database,
        schema=schema,
        table=table,
        structure=structure,
        show_constraints=show_constraints
    )


def create_query_result(
    sql: str,
    results: List[Dict[str, Any]],
    database: str
) -> QueryResult:
    """Create a QueryResult instance."""
    return QueryResult(
        command="query",
        timestamp=datetime.now(),
        database=database,
        sql=sql,
        results=results,
        row_count=len(results)
    )


def create_info_result(db_info: Dict[str, Any], database: str) -> InfoResult:
    """Create an InfoResult instance."""
    info = DatabaseInfo(
        database_name=db_info.get('database_name', ''),
        current_user=db_info.get('current_user', ''),
        version=db_info.get('version', ''),
        encoding=db_info.get('encoding', ''),
        timezone=db_info.get('timezone', ''),
        timestamp=datetime.now()
    )

    return InfoResult(
        command="info",
        timestamp=datetime.now(),
        database=database,
        info=info
    )


def output_json(result: CatalogResult, indent: Optional[int] = 2) -> str:
    """Output a catalog result as formatted JSON."""
    return result.as_json(indent=indent)


def save_json_to_file(result: CatalogResult, filename: str, indent: Optional[int] = 2) -> None:
    """Save a catalog result to a JSON file."""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(result.as_json(indent=indent))
