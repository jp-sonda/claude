"""
PostgreSQL catalog navigation and inspection module.
"""

import logging
from typing import Optional, List, Dict, Any, Tuple
import psycopg2
from psycopg2 import sql

logger = logging.getLogger(__name__)


class DatabaseConnectionError(Exception):
    """Raised when database connection fails"""
    pass


class QueryExecutionError(Exception):
    """Raised when query execution fails"""
    pass


class PostgreSQLCatalog:
    """
    PostgreSQL catalog navigator for inspecting database schemas, tables, and constraints.

    This class provides methods to connect to a PostgreSQL database and retrieve
    metadata about schemas, tables, columns, indexes, and integrity constraints.
    """

    def __init__(self, connection_string: str):
        """
        Initialize the catalog with a connection string.

        Args:
            connection_string: PostgreSQL connection string in the format:
                postgresql://username:password@host:port/database
        """
        self.connection_string = connection_string
        self.connection: Optional[psycopg2.extensions.connection] = None

    def connect(self) -> bool:
        """
        Establish connection to PostgreSQL database.

        Returns:
            True if connection successful, False otherwise

        Raises:
            DatabaseConnectionError: If connection fails
        """
        try:
            self.connection = psycopg2.connect(self.connection_string)
            logger.info("Successfully connected to PostgreSQL database")
            return True
        except psycopg2.Error as e:
            logger.error(f"Database connection failed: {e}")
            raise DatabaseConnectionError(f"Failed to connect to database: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during connection: {e}")
            raise DatabaseConnectionError(f"Unexpected connection error: {e}")

    def disconnect(self) -> None:
        """Close database connection."""
        if self.connection:
            try:
                self.connection.close()
                logger.info("Database connection closed")
            except Exception as e:
                logger.warning(f"Error closing database connection: {e}")
            finally:
                self.connection = None

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()

    def execute_query(self, query: str, params: Optional[Tuple] = None) -> List[Dict[str, Any]]:
        """
        Execute query and return results as list of dictionaries.

        Args:
            query: SQL query string
            params: Query parameters tuple

        Returns:
            List of dictionaries with column names as keys

        Raises:
            QueryExecutionError: If query execution fails
        """
        if not self.connection:
            raise QueryExecutionError("No database connection available")

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)

            # Get column names
            columns = [desc[0] for desc in cursor.description] if cursor.description else []

            # Fetch all results
            rows = cursor.fetchall()

            # Convert to list of dictionaries
            results = []
            for row in rows:
                results.append(dict(zip(columns, row)))

            cursor.close()
            logger.debug(f"Query executed successfully, returned {len(results)} rows")
            return results

        except psycopg2.Error as e:
            logger.error(f"Query execution failed: {e}")
            raise QueryExecutionError(f"Query execution failed: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during query execution: {e}")
            raise QueryExecutionError(f"Unexpected query error: {e}")

    def list_schemas(self) -> List[Dict[str, Any]]:
        """
        List all user-defined schemas in the database.

        Returns:
            List of dictionaries containing schema information
        """
        query = """
        SELECT
            schema_name,
            schema_owner
        FROM information_schema.schemata
        WHERE schema_name NOT IN ('information_schema', 'pg_catalog', 'pg_toast')
        ORDER BY schema_name;
        """
        return self.execute_query(query)

    def list_tables(self, schema_name: str = 'public') -> List[Dict[str, Any]]:
        """
        List all tables in a specific schema.

        Args:
            schema_name: Name of the schema to inspect

        Returns:
            List of dictionaries containing table information
        """
        query = """
        SELECT
            table_name,
            table_type,
            table_schema
        FROM information_schema.tables
        WHERE table_schema = %s
        ORDER BY table_name;
        """
        return self.execute_query(query, (schema_name,))

    def describe_table(self, table_name: str, schema_name: str = 'public') -> List[Dict[str, Any]]:
        """
        Get detailed column information for a table.

        Args:
            table_name: Name of the table to describe
            schema_name: Schema containing the table

        Returns:
            List of dictionaries containing column information
        """
        query = """
        SELECT
            column_name,
            data_type,
            is_nullable,
            column_default,
            character_maximum_length,
            numeric_precision,
            numeric_scale
        FROM information_schema.columns
        WHERE table_name = %s AND table_schema = %s
        ORDER BY ordinal_position;
        """
        return self.execute_query(query, (table_name, schema_name))

    def list_indexes(self, table_name: str, schema_name: str = 'public') -> List[Dict[str, Any]]:
        """
        List all indexes for a specific table.

        Args:
            table_name: Name of the table
            schema_name: Schema containing the table

        Returns:
            List of dictionaries containing index information
        """
        query = """
        SELECT
            i.relname AS index_name,
            a.attname AS column_name,
            ix.indisunique AS is_unique,
            ix.indisprimary AS is_primary
        FROM
            pg_class t,
            pg_class i,
            pg_index ix,
            pg_attribute a,
            pg_namespace n
        WHERE
            t.oid = ix.indrelid
            AND i.oid = ix.indexrelid
            AND a.attrelid = t.oid
            AND a.attnum = ANY(ix.indkey)
            AND t.relkind = 'r'
            AND t.relname = %s
            AND n.nspname = %s
            AND n.oid = t.relnamespace
        ORDER BY i.relname, a.attnum;
        """
        return self.execute_query(query, (table_name, schema_name))

    def list_constraints(self, table_name: str, schema_name: str = 'public') -> List[Dict[str, Any]]:
        """
        List all integrity constraints for a table.

        Args:
            table_name: Name of the table
            schema_name: Schema containing the table

        Returns:
            List of dictionaries containing constraint information
        """
        query = """
        SELECT
            tc.constraint_name,
            tc.constraint_type,
            tc.table_name,
            tc.table_schema,
            kcu.column_name,
            CASE
                WHEN tc.constraint_type = 'FOREIGN KEY' THEN
                    ccu.table_schema || '.' || ccu.table_name || '.' || ccu.column_name
                ELSE NULL
            END AS foreign_table_column,
            CASE
                WHEN tc.constraint_type = 'CHECK' THEN cc.check_clause
                ELSE NULL
            END AS check_clause,
            tc.is_deferrable,
            tc.initially_deferred
        FROM
            information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu
                ON tc.constraint_name = kcu.constraint_name
                AND tc.table_schema = kcu.table_schema
            LEFT JOIN information_schema.constraint_column_usage AS ccu
                ON ccu.constraint_name = tc.constraint_name
                AND ccu.table_schema = tc.table_schema
            LEFT JOIN information_schema.check_constraints AS cc
                ON cc.constraint_name = tc.constraint_name
                AND cc.constraint_schema = tc.table_schema
        WHERE
            tc.table_name = %s
            AND tc.table_schema = %s
        ORDER BY
            CASE tc.constraint_type
                WHEN 'PRIMARY KEY' THEN 1
                WHEN 'FOREIGN KEY' THEN 2
                WHEN 'UNIQUE' THEN 3
                WHEN 'CHECK' THEN 4
                ELSE 5
            END,
            tc.constraint_name,
            kcu.ordinal_position;
        """
        return self.execute_query(query, (table_name, schema_name))

    def get_foreign_key_details(self, table_name: str, schema_name: str = 'public') -> List[Dict[str, Any]]:
        """
        Get detailed foreign key information including referential actions.

        Args:
            table_name: Name of the table
            schema_name: Schema containing the table

        Returns:
            List of dictionaries containing foreign key details
        """
        query = """
        SELECT
            tc.constraint_name,
            kcu.column_name AS column_name,
            ccu.table_schema AS foreign_table_schema,
            ccu.table_name AS foreign_table_name,
            ccu.column_name AS foreign_column_name,
            rc.update_rule AS on_update,
            rc.delete_rule AS on_delete,
            tc.is_deferrable,
            tc.initially_deferred
        FROM
            information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu
                ON tc.constraint_name = kcu.constraint_name
                AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage AS ccu
                ON ccu.constraint_name = tc.constraint_name
                AND ccu.table_schema = tc.table_schema
            JOIN information_schema.referential_constraints AS rc
                ON tc.constraint_name = rc.constraint_name
                AND tc.table_schema = rc.constraint_schema
        WHERE
            tc.constraint_type = 'FOREIGN KEY'
            AND tc.table_name = %s
            AND tc.table_schema = %s
        ORDER BY tc.constraint_name, kcu.ordinal_position;
        """
        return self.execute_query(query, (table_name, schema_name))

    def get_database_info(self) -> Dict[str, Any]:
        """
        Get general database information.

        Returns:
            Dictionary containing database metadata
        """
        query = """
        SELECT
            current_database() as database_name,
            current_user as current_user,
            version() as version,
            current_setting('server_encoding') as encoding,
            current_setting('TimeZone') as timezone;
        """
        result = self.execute_query(query)
        return result[0] if result else {}

    def table_exists(self, table_name: str, schema_name: str = 'public') -> bool:
        """
        Check if a table exists in the specified schema.

        Args:
            table_name: Name of the table to check
            schema_name: Schema to check in

        Returns:
            True if table exists, False otherwise
        """
        query = """
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = %s AND table_name = %s
        );
        """
        result = self.execute_query(query, (schema_name, table_name))
        return result[0]['exists'] if result else False

    def schema_exists(self, schema_name: str) -> bool:
        """
        Check if a schema exists.

        Args:
            schema_name: Name of the schema to check

        Returns:
            True if schema exists, False otherwise
        """
        query = """
        SELECT EXISTS (
            SELECT FROM information_schema.schemata
            WHERE schema_name = %s
        );
        """
        result = self.execute_query(query, (schema_name,))
        return result[0]['exists'] if result else False
