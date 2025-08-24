"""
Tests for the PostgreSQLCatalog class.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from psql_catalog.catalog import PostgreSQLCatalog, DatabaseConnectionError, QueryExecutionError


class TestPostgreSQLCatalog:
    """Test cases for PostgreSQLCatalog class."""

    def test_init(self):
        """Test catalog initialization."""
        connection_string = "postgresql://user:pass@localhost:5432/testdb"
        catalog = PostgreSQLCatalog(connection_string)

        assert catalog.connection_string == connection_string
        assert catalog.connection is None

    @patch('psql_catalog.catalog.psycopg2.connect')
    def test_connect_success(self, mock_connect):
        """Test successful database connection."""
        mock_connection = Mock()
        mock_connect.return_value = mock_connection

        catalog = PostgreSQLCatalog("postgresql://user:pass@localhost:5432/testdb")
        result = catalog.connect()

        assert result is True
        assert catalog.connection == mock_connection
        mock_connect.assert_called_once()

    @patch('psql_catalog.catalog.psycopg2.connect')
    def test_connect_failure(self, mock_connect):
        """Test database connection failure."""
        mock_connect.side_effect = Exception("Connection failed")

        catalog = PostgreSQLCatalog("postgresql://user:pass@localhost:5432/testdb")

        with pytest.raises(DatabaseConnectionError):
            catalog.connect()

    def test_disconnect(self):
        """Test database disconnection."""
        catalog = PostgreSQLCatalog("postgresql://user:pass@localhost:5432/testdb")
        mock_connection = Mock()
        catalog.connection = mock_connection

        catalog.disconnect()

        mock_connection.close.assert_called_once()
        assert catalog.connection is None

    def test_context_manager(self):
        """Test catalog as context manager."""
        catalog = PostgreSQLCatalog("postgresql://user:pass@localhost:5432/testdb")

        with patch.object(catalog, 'connect') as mock_connect:
            with patch.object(catalog, 'disconnect') as mock_disconnect:
                with catalog:
                    pass

                mock_connect.assert_called_once()
                mock_disconnect.assert_called_once()

    def test_execute_query_no_connection(self):
        """Test query execution without connection."""
        catalog = PostgreSQLCatalog("postgresql://user:pass@localhost:5432/testdb")

        with pytest.raises(QueryExecutionError, match="No database connection"):
            catalog.execute_query("SELECT 1")

    @patch('psql_catalog.catalog.psycopg2.connect')
    def test_execute_query_success(self, mock_connect):
        """Test successful query execution."""
        # Setup mock connection and cursor
        mock_cursor = Mock()
        mock_cursor.description = [('column1',), ('column2',)]
        mock_cursor.fetchall.return_value = [('value1', 'value2')]

        mock_connection = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        catalog = PostgreSQLCatalog("postgresql://user:pass@localhost:5432/testdb")
        catalog.connect()

        result = catalog.execute_query("SELECT column1, column2 FROM test")

        expected = [{'column1': 'value1', 'column2': 'value2'}]
        assert result == expected
        mock_cursor.execute.assert_called_once_with("SELECT column1, column2 FROM test", None)
        mock_cursor.close.assert_called_once()

    @patch('psql_catalog.catalog.psycopg2.connect')
    def test_table_exists_true(self, mock_connect):
        """Test table_exists method when table exists."""
        mock_cursor = Mock()
        mock_cursor.description = [('exists',)]
        mock_cursor.fetchall.return_value = [(True,)]

        mock_connection = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        catalog = PostgreSQLCatalog("postgresql://user:pass@localhost:5432/testdb")
        catalog.connect()

        result = catalog.table_exists('users', 'public')

        assert result is True

    @patch('psql_catalog.catalog.psycopg2.connect')
    def test_table_exists_false(self, mock_connect):
        """Test table_exists method when table doesn't exist."""
        mock_cursor = Mock()
        mock_cursor.description = [('exists',)]
        mock_cursor.fetchall.return_value = [(False,)]

        mock_connection = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        catalog = PostgreSQLCatalog("postgresql://user:pass@localhost:5432/testdb")
        catalog.connect()

        result = catalog.table_exists('nonexistent', 'public')

        assert result is False

    @patch('psql_catalog.catalog.psycopg2.connect')
    def test_schema_exists_true(self, mock_connect):
        """Test schema_exists method when schema exists."""
        mock_cursor = Mock()
        mock_cursor.description = [('exists',)]
        mock_cursor.fetchall.return_value = [(True,)]

        mock_connection = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        catalog = PostgreSQLCatalog("postgresql://user:pass@localhost:5432/testdb")
        catalog.connect()

        result = catalog.schema_exists('public')

        assert result is True

    @patch('psql_catalog.catalog.psycopg2.connect')
    def test_get_database_info(self, mock_connect):
        """Test get_database_info method."""
        mock_cursor = Mock()
        mock_cursor.description = [
            ('database_name',), ('current_user',), ('version',),
            ('encoding',), ('timezone',)
        ]
        mock_cursor.fetchall.return_value = [
            ('testdb', 'testuser', 'PostgreSQL 14.0', 'UTF8', 'UTC')
        ]

        mock_connection = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        catalog = PostgreSQLCatalog("postgresql://user:pass@localhost:5432/testdb")
        catalog.connect()

        result = catalog.get_database_info()

        expected = {
            'database_name': 'testdb',
            'current_user': 'testuser',
            'version': 'PostgreSQL 14.0',
            'encoding': 'UTF8',
            'timezone': 'UTC'
        }
        assert result == expected


if __name__ == "__main__":
    pytest.main([__file__])
