"""
Tests for the serialization module.
"""

import json
import pytest
from datetime import datetime
from psql_catalog.serialization import (
    JSONSerializableMixin,
    CatalogResult,
    SchemasResult,
    TablesResult,
    DescribeResult,
    QueryResult,
    InfoResult,
    TableStructure,
    DatabaseInfo,
    create_schemas_result,
    create_tables_result,
    create_describe_result,
    create_query_result,
    create_info_result,
    output_json
)


class TestJSONSerializableMixin:
    """Test cases for JSONSerializableMixin."""

    def test_as_json(self):
        """Test JSON serialization."""

        class TestClass(JSONSerializableMixin):
            def __init__(self, name: str, value: int):
                self.name = name
                self.value = value

        obj = TestClass("test", 42)
        json_str = obj.as_json()

        # Parse to verify valid JSON
        parsed = json.loads(json_str)
        assert parsed["name"] == "test"
        assert parsed["value"] == 42

    def test_from_json(self):
        """Test JSON deserialization."""

        class TestClass(JSONSerializableMixin):
            def __init__(self, name: str, value: int):
                self.name = name
                self.value = value

        json_str = '{"name": "test", "value": 42}'
        obj = TestClass.from_json(json_str)

        assert obj.name == "test"
        assert obj.value == 42

    def test_datetime_serialization(self):
        """Test datetime serialization."""

        class TestClass(JSONSerializableMixin):
            def __init__(self, timestamp: datetime):
                self.timestamp = timestamp

        now = datetime.now()
        obj = TestClass(now)
        json_str = obj.as_json()

        # Parse to verify valid JSON
        parsed = json.loads(json_str)
        assert parsed["timestamp"] == now.isoformat()


class TestCatalogResults:
    """Test cases for catalog result classes."""

    def test_schemas_result_creation(self):
        """Test SchemasResult creation and serialization."""
        schemas_data = [
            {"schema_name": "public", "schema_owner": "postgres"},
            {"schema_name": "test", "schema_owner": "testuser"}
        ]

        result = create_schemas_result(schemas_data, "testdb")

        assert result.command == "schemas"
        assert result.database == "testdb"
        assert result.schemas == schemas_data
        assert isinstance(result.timestamp, datetime)

        # Test JSON serialization
        json_str = result.as_json()
        parsed = json.loads(json_str)

        assert parsed["command"] == "schemas"
        assert parsed["database"] == "testdb"
        assert parsed["schemas"] == schemas_data

    def test_tables_result_creation(self):
        """Test TablesResult creation and serialization."""
        tables_data = [
            {"table_name": "users", "table_type": "BASE TABLE", "table_schema": "public"},
            {"table_name": "orders", "table_type": "BASE TABLE", "table_schema": "public"}
        ]

        result = create_tables_result(tables_data, "testdb", "public")

        assert result.command == "tables"
        assert result.database == "testdb"
        assert result.schema == "public"
        assert result.tables == tables_data

        # Test JSON serialization
        json_str = result.as_json()
        parsed = json.loads(json_str)

        assert parsed["schema"] == "public"
        assert parsed["tables"] == tables_data

    def test_describe_result_creation(self):
        """Test DescribeResult creation and serialization."""
        columns_data = [
            {"column_name": "id", "data_type": "integer", "is_nullable": "NO"},
            {"column_name": "name", "data_type": "varchar", "is_nullable": "YES"}
        ]
        indexes_data = [
            {"index_name": "users_pkey", "column_name": "id", "is_unique": True}
        ]

        result = create_describe_result(
            columns=columns_data,
            indexes=indexes_data,
            database="testdb",
            schema="public",
            table="users"
        )

        assert result.command == "describe"
        assert result.database == "testdb"
        assert result.schema == "public"
        assert result.table == "users"
        assert result.structure.columns == columns_data
        assert result.structure.indexes == indexes_data
        assert result.structure.constraints is None  # Not requested

        # Test JSON serialization
        json_str = result.as_json()
        parsed = json.loads(json_str)

        assert parsed["table"] == "users"
        assert parsed["structure"]["columns"] == columns_data
        assert parsed["structure"]["indexes"] == indexes_data

    def test_describe_result_with_constraints(self):
        """Test DescribeResult with constraints."""
        columns_data = [{"column_name": "id", "data_type": "integer"}]
        indexes_data = [{"index_name": "users_pkey", "column_name": "id"}]
        constraints_data = [{"constraint_name": "users_pkey", "constraint_type": "PRIMARY KEY"}]
        fk_details = []

        result = create_describe_result(
            columns=columns_data,
            indexes=indexes_data,
            database="testdb",
            schema="public",
            table="users",
            show_constraints=True,
            constraints=constraints_data,
            foreign_key_details=fk_details
        )

        assert result.show_constraints is True
        assert result.structure.constraints == constraints_data
        assert result.structure.foreign_key_details == fk_details

    def test_query_result_creation(self):
        """Test QueryResult creation and serialization."""
        query_results = [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"}
        ]
        sql = "SELECT id, name FROM users LIMIT 2"

        result = create_query_result(sql, query_results, "testdb")

        assert result.command == "query"
        assert result.database == "testdb"
        assert result.sql == sql
        assert result.results == query_results
        assert result.row_count == 2

        # Test JSON serialization
        json_str = result.as_json()
        parsed = json.loads(json_str)

        assert parsed["sql"] == sql
        assert parsed["row_count"] == 2
        assert parsed["results"] == query_results

    def test_info_result_creation(self):
        """Test InfoResult creation and serialization."""
        db_info = {
            "database_name": "testdb",
            "current_user": "postgres",
            "version": "PostgreSQL 14.0",
            "encoding": "UTF8",
            "timezone": "UTC"
        }

        result = create_info_result(db_info, "testdb")

        assert result.command == "info"
        assert result.database == "testdb"
        assert result.info.database_name == "testdb"
        assert result.info.current_user == "postgres"

        # Test JSON serialization
        json_str = result.as_json()
        parsed = json.loads(json_str)

        assert parsed["info"]["database_name"] == "testdb"
        assert parsed["info"]["version"] == "PostgreSQL 14.0"


class TestTableStructure:
    """Test cases for TableStructure."""

    def test_table_structure_serialization(self):
        """Test TableStructure JSON serialization."""
        columns = [{"column_name": "id", "data_type": "integer"}]
        indexes = [{"index_name": "test_idx", "column_name": "id"}]

        structure = TableStructure(columns=columns, indexes=indexes)

        json_str = structure.as_json()
        parsed = json.loads(json_str)

        assert parsed["columns"] == columns
        assert parsed["indexes"] == indexes
        assert parsed["constraints"] is None

    def test_table_structure_with_constraints(self):
        """Test TableStructure with constraints."""
        columns = [{"column_name": "id", "data_type": "integer"}]
        indexes = [{"index_name": "test_idx", "column_name": "id"}]
        constraints = [{"constraint_name": "pk_test", "constraint_type": "PRIMARY KEY"}]
        fk_details = [{"constraint_name": "fk_test", "on_delete": "CASCADE"}]

        structure = TableStructure(
            columns=columns,
            indexes=indexes,
            constraints=constraints,
            foreign_key_details=fk_details
        )

        json_str = structure.as_json()
        parsed = json.loads(json_str)

        assert parsed["constraints"] == constraints
        assert parsed["foreign_key_details"] == fk_details


class TestDatabaseInfo:
    """Test cases for DatabaseInfo."""

    def test_database_info_serialization(self):
        """Test DatabaseInfo JSON serialization."""
        now = datetime.now()

        info = DatabaseInfo(
            database_name="testdb",
            current_user="postgres",
            version="PostgreSQL 14.0",
            encoding="UTF8",
            timezone="UTC",
            timestamp=now
        )

        json_str = info.as_json()
        parsed = json.loads(json_str)

        assert parsed["database_name"] == "testdb"
        assert parsed["current_user"] == "postgres"
        assert parsed["timestamp"] == now.isoformat()


class TestUtilityFunctions:
    """Test cases for utility functions."""

    def test_output_json(self):
        """Test output_json function."""
        schemas_data = [{"schema_name": "public", "schema_owner": "postgres"}]
        result = create_schemas_result(schemas_data, "testdb")

        json_str = output_json(result)

        # Should be valid JSON
        parsed = json.loads(json_str)
        assert parsed["command"] == "schemas"
        assert parsed["database"] == "testdb"

        # Test with custom indentation
        json_str_compact = output_json(result, indent=None)
        json_str_pretty = output_json(result, indent=4)

        # Compact should be shorter
        assert len(json_str_compact) < len(json_str_pretty)


if __name__ == "__main__":
    pytest.main([__file__])
