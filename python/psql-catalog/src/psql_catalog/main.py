#!/usr/bin/env python3

"""
psql-catalog: A PostgreSQL catalog navigator for database schemas
"""

import os
import sys
from typing import Optional, List, Dict, Any
import psycopg2
from psycopg2 import sql
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from tabulate import tabulate

app = typer.Typer(help="Navigate PostgreSQL database catalogs and schemas")
console = Console()


class PostgreSQLCatalog:
    """PostgreSQL catalog navigator"""

    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connection = None

    def connect(self) -> bool:
        """Establish connection to PostgreSQL database"""
        try:
            self.connection = psycopg2.connect(self.connection_string)
            return True
        except Exception as e:
            console.print(f"[red]Error connecting to database: {e}[/red]")
            return False

    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()

    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """Execute query and return results"""
        if not self.connection:
            console.print("[red]No database connection[/red]")
            return []

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
            return results

        except Exception as e:
            console.print(f"[red]Error executing query: {e}[/red]")
            return []

    def list_schemas(self) -> List[Dict[str, Any]]:
        """List all schemas in the database"""
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
        """List all tables in a schema"""
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
        """Describe table structure"""
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
        """List indexes for a table"""
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


def display_table(data: List[Dict[str, Any]], title: str):
    """Display data in a rich table format"""
    if not data:
        console.print(f"[yellow]No {title.lower()} found[/yellow]")
        return

    table = Table(title=title, show_header=True, header_style="bold magenta")

    # Add columns
    if data:
        for column in data[0].keys():
            table.add_column(column.replace('_', ' ').title())

        # Add rows
        for row in data:
            table.add_row(*[str(value) if value is not None else "" for value in row.values()])

    console.print(table)


@app.command()
def schemas(connection_string: str = typer.Option(..., "--db", "-d", help="PostgreSQL connection string")):
    """List all schemas in the database"""
    catalog = PostgreSQLCatalog(connection_string)
    if catalog.connect():
        schemas_data = catalog.list_schemas()
        display_table(schemas_data, "Database Schemas")
        catalog.disconnect()


@app.command()
def tables(
    schema: str = typer.Option("public", "--schema", "-s", help="Schema name"),
    connection_string: str = typer.Option(..., "--db", "-d", help="PostgreSQL connection string")
):
    """List all tables in a schema"""
    catalog = PostgreSQLCatalog(connection_string)
    if catalog.connect():
        tables_data = catalog.list_tables(schema)
        display_table(tables_data, f"Tables in '{schema}' Schema")
        catalog.disconnect()


@app.command()
def describe(
    table: str = typer.Argument(..., help="Table name to describe"),
    schema: str = typer.Option("public", "--schema", "-s", help="Schema name"),
    connection_string: str = typer.Option(..., "--db", "-d", help="PostgreSQL connection string")
):
    """Describe table structure"""
    catalog = PostgreSQLCatalog(connection_string)
    if catalog.connect():
        columns_data = catalog.describe_table(table, schema)
        display_table(columns_data, f"Structure of '{schema}.{table}'")

        # Also show indexes
        indexes_data = catalog.list_indexes(table, schema)
        if indexes_data:
            console.print("\n")
            display_table(indexes_data, f"Indexes for '{schema}.{table}'")

        catalog.disconnect()


@app.command()
def interactive():
    """Interactive mode for exploring database catalog"""
    connection_string = typer.prompt("Enter PostgreSQL connection string")

    catalog = PostgreSQLCatalog(connection_string)
    if not catalog.connect():
        return

    console.print("[green]Connected to PostgreSQL database![/green]")
    console.print("Type 'help' for available commands or 'quit' to exit")

    while True:
        try:
            command = typer.prompt("\npsql-catalog>", default="").strip()

            if command.lower() in ['quit', 'exit', 'q']:
                break
            elif command.lower() in ['help', 'h']:
                console.print("""
Available commands:
- schemas: List all schemas
- tables [schema]: List tables in schema (default: public)
- describe <table> [schema]: Describe table structure
- query <sql>: Execute custom SQL query
- help: Show this help
- quit: Exit interactive mode
                """)
            elif command.lower() == 'schemas':
                schemas_data = catalog.list_schemas()
                display_table(schemas_data, "Database Schemas")
            elif command.startswith('tables'):
                parts = command.split()
                schema_name = parts[1] if len(parts) > 1 else 'public'
                tables_data = catalog.list_tables(schema_name)
                display_table(tables_data, f"Tables in '{schema_name}' Schema")
            elif command.startswith('describe'):
                parts = command.split()
                if len(parts) < 2:
                    console.print("[red]Usage: describe <table> [schema][/red]")
                    continue
                table_name = parts[1]
                schema_name = parts[2] if len(parts) > 2 else 'public'

                columns_data = catalog.describe_table(table_name, schema_name)
                display_table(columns_data, f"Structure of '{schema_name}.{table_name}'")

                indexes_data = catalog.list_indexes(table_name, schema_name)
                if indexes_data:
                    console.print("\n")
                    display_table(indexes_data, f"Indexes for '{schema_name}.{table_name}'")
            elif command.startswith('query'):
                sql_query = command[5:].strip()  # Remove 'query' prefix
                if sql_query:
                    results = catalog.execute_query(sql_query)
                    if results:
                        display_table(results, "Query Results")
                else:
                    console.print("[red]Usage: query <sql>[/red]")
            elif command:
                console.print(f"[red]Unknown command: {command}[/red]")
                console.print("Type 'help' for available commands")

        except KeyboardInterrupt:
            console.print("\n[yellow]Use 'quit' to exit[/yellow]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

    catalog.disconnect()
    console.print("[green]Goodbye![/green]")


def main():
    """Main entry point"""
    app()


if __name__ == "__main__":
    main()
