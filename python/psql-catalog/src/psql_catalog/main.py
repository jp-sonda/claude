#!/usr/bin/env python3
"""
psql-catalog: A PostgreSQL catalog navigator for database schemas

Command-line interface for exploring PostgreSQL database catalogs.
"""

import logging
import sys
from typing import Optional
from datetime import datetime
import typer

from .catalog import PostgreSQLCatalog, DatabaseConnectionError, QueryExecutionError
from .display import (
    display_table,
    display_constraints,
    display_database_info,
    display_help,
    display_json,
    display_json_raw,
    display_describe_all,
    print_success,
    print_error,
    print_warning,
    console
)
from .exceptions import TableNotFoundError, SchemaNotFoundError
from .serialization import (
    create_schemas_result,
    create_tables_result,
    create_describe_result,
    create_describe_all_result,
    create_query_result,
    create_info_result,
    output_json,
    save_json_to_file,
    TableStructure,
    DescribeAllResult
)

# Configure logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

app = typer.Typer(help="Navigate PostgreSQL database catalogs and schemas")

def validate_connection_string(connection_string: str) -> bool:
    """
    Basic validation of PostgreSQL connection string format.

    Args:
        connection_string: Connection string to validate

    Returns:
        True if format appears valid
    """
    required_parts = ['postgresql://', '@', ':', '/']
    return all(part in connection_string for part in required_parts)

@app.command()
def schemas(
    connection_string: str = typer.Option(..., "--db", "-d", help="PostgreSQL connection string"),
    json_output: bool = typer.Option(False, "--json", "-j", help="Output results as JSON"),
    output_file: Optional[str] = typer.Option(None, "--output", "-o", help="Save output to file")
):
    """List all schemas in the database"""
    if not validate_connection_string(connection_string):
        print_error("Invalid connection string format. Expected: postgresql://user:password@host:port/database")
        raise typer.Exit(1)

    try:
        with PostgreSQLCatalog(connection_string) as catalog:
            schemas_data = catalog.list_schemas()

            if json_output:
                result = create_schemas_result(schemas_data, catalog.database_name)
                if output_file:
                    save_json_to_file(result, output_file)
                    print_success(f"Schemas saved to {output_file}")
                else:
                    display_json(result)
            else:
                display_table(schemas_data, "Database Schemas")

    except DatabaseConnectionError as e:
        print_error(f"Connection failed: {e}")
        raise typer.Exit(1)
    except QueryExecutionError as e:
        print_error(f"Query failed: {e}")

def _handle_describe_all_command(catalog: PostgreSQLCatalog, command: str, json_mode: bool = False) -> None:
    """Handle the 'describe-all' command in interactive mode."""
    parts = command.split()
    schema_name = 'public'
    show_constraints = False

    # Parse additional parameters
    for i, part in enumerate(parts[1:], 1):
        if part.startswith('--'):
            if part in ['--constraints', '-c']:
                show_constraints = True
        else:
            schema_name = part

    try:
        if not catalog.schema_exists(schema_name):
            print_error(f"Schema '{schema_name}' does not exist")
            return

        # Get all tables in schema
        tables_list = catalog.list_tables(schema_name)
        
        if not tables_list:
            print_warning(f"No tables found in schema '{schema_name}'")
            return

        # Process each table
        tables_data = {}
        failed_tables = []
        
        for table_info in tables_list:
            table_name = table_info['table_name']
            
            try:
                # Get table information
                columns_data = catalog.describe_table(table_name, schema_name)
                indexes_data = catalog.list_indexes(table_name, schema_name)
                
                constraints_data = None
                fk_details = None
                if show_constraints:
                    constraints_data = catalog.list_constraints(table_name, schema_name)
                    fk_details = catalog.get_foreign_key_details(table_name, schema_name)
                
                # Create table structure
                table_structure = TableStructure(
                    columns=columns_data,
                    indexes=indexes_data,
                    constraints=constraints_data,
                    foreign_key_details=fk_details
                )
                
                tables_data[table_name] = table_structure
                
            except Exception as e:
                print_warning(f"Failed to describe table '{schema_name}.{table_name}': {e}")
                failed_tables.append(table_name)
                continue

        if json_mode:
            result = create_describe_all_result(
                tables_data=tables_data,
                database=catalog.database_name,
                schema=schema_name,
                show_constraints=show_constraints,
                failed_tables=failed_tables
            )
            display_json(result)
        else:
            # Display in text format
            result = DescribeAllResult(
                command="describe-all",
                timestamp=datetime.now(),
                database=catalog.database_name,
                schema=schema_name,
                tables=tables_data,
                show_constraints=show_constraints,
                total_tables=len(tables_data),
                failed_tables=failed_tables
            )
            
            display_describe_all(result)

    except QueryExecutionError as e:
        print_error(f"Failed to describe schema: {e}")

@app.command()
def tables(
    schema: str = typer.Option("public", "--schema", "-s", help="Schema name"),
    connection_string: str = typer.Option(..., "--db", "-d", help="PostgreSQL connection string"),
    json_output: bool = typer.Option(False, "--json", "-j", help="Output results as JSON"),
    output_file: Optional[str] = typer.Option(None, "--output", "-o", help="Save output to file")
):
    """List all tables in a schema"""
    if not validate_connection_string(connection_string):
        print_error("Invalid connection string format. Expected: postgresql://user:password@host:port/database")
        raise typer.Exit(1)

    try:
        with PostgreSQLCatalog(connection_string) as catalog:
            # Check if schema exists
            if not catalog.schema_exists(schema):
                print_error(f"Schema '{schema}' does not exist")
                raise typer.Exit(1)

            tables_data = catalog.list_tables(schema)

            if json_output:
                result = create_tables_result(tables_data, catalog.database_name, schema)
                if output_file:
                    save_json_to_file(result, output_file)
                    print_success(f"Tables saved to {output_file}")
                else:
                    display_json(result)
            else:
                display_table(tables_data, f"Tables in '{schema}' Schema")

    except DatabaseConnectionError as e:
        print_error(f"Connection failed: {e}")
        raise typer.Exit(1)
    except QueryExecutionError as e:
        print_error(f"Query failed: {e}")
        raise typer.Exit(1)

@app.command("describe-all")
def describe_all(
    schema: str = typer.Option("public", "--schema", "-s", help="Schema name"),
    constraints: bool = typer.Option(False, "--constraints", "-c", help="Show integrity constraints"),
    connection_string: str = typer.Option(..., "--db", "-d", help="PostgreSQL connection string"),
    json_output: bool = typer.Option(False, "--json", "-j", help="Output results as JSON"),
    output_file: Optional[str] = typer.Option(None, "--output", "-o", help="Save output to file")
):
    """Describe all tables in a schema"""
    if not validate_connection_string(connection_string):
        print_error("Invalid connection string format. Expected: postgresql://user:password@host:port/database")
        raise typer.Exit(1)

    try:
        with PostgreSQLCatalog(connection_string) as catalog:
            # Check if schema exists
            if not catalog.schema_exists(schema):
                print_error(f"Schema '{schema}' does not exist")
                raise typer.Exit(1)

            # Get all tables in schema
            tables_list = catalog.list_tables(schema)
            
            if not tables_list:
                print_warning(f"No tables found in schema '{schema}'")
                return

            # Process each table
            tables_data = {}
            failed_tables = []
            
            for table_info in tables_list:
                table_name = table_info['table_name']
                
                try:
                    # Get table information
                    columns_data = catalog.describe_table(table_name, schema)
                    indexes_data = catalog.list_indexes(table_name, schema)
                    
                    constraints_data = None
                    fk_details = None
                    if constraints:
                        constraints_data = catalog.list_constraints(table_name, schema)
                        fk_details = catalog.get_foreign_key_details(table_name, schema)
                    
                    # Create table structure
                    table_structure = TableStructure(
                        columns=columns_data,
                        indexes=indexes_data,
                        constraints=constraints_data,
                        foreign_key_details=fk_details
                    )
                    
                    tables_data[table_name] = table_structure
                    
                except Exception as e:
                    print_warning(f"Failed to describe table '{schema}.{table_name}': {e}")
                    failed_tables.append(table_name)
                    continue

            if json_output:
                result = create_describe_all_result(
                    tables_data=tables_data,
                    database=catalog.database_name,
                    schema=schema,
                    show_constraints=constraints,
                    failed_tables=failed_tables
                )
                
                if output_file:
                    save_json_to_file(result, output_file)
                    print_success(f"Schema description saved to {output_file}")
                else:
                    display_json(result)
            else:
                # Display in text format
                result = DescribeAllResult(
                    command="describe-all",
                    timestamp=datetime.now(),
                    database=catalog.database_name,
                    schema=schema,
                    tables=tables_data,
                    show_constraints=constraints,
                    total_tables=len(tables_data),
                    failed_tables=failed_tables
                )
                
                display_describe_all(result)

    except DatabaseConnectionError as e:
        print_error(f"Connection failed: {e}")
        raise typer.Exit(1)
    except QueryExecutionError as e:
        print_error(f"Query failed: {e}")
        raise typer.Exit(1)

@app.command()
def describe(
    table: str = typer.Argument(..., help="Table name to describe"),
    schema: str = typer.Option("public", "--schema", "-s", help="Schema name"),
    constraints: bool = typer.Option(False, "--constraints", "-c", help="Show integrity constraints"),
    connection_string: str = typer.Option(..., "--db", "-d", help="PostgreSQL connection string"),
    json_output: bool = typer.Option(False, "--json", "-j", help="Output results as JSON"),
    output_file: Optional[str] = typer.Option(None, "--output", "-o", help="Save output to file")
):
    """Describe table structure"""
    if not validate_connection_string(connection_string):
        print_error("Invalid connection string format. Expected: postgresql://user:password@host:port/database")
        raise typer.Exit(1)

    try:
        with PostgreSQLCatalog(connection_string) as catalog:
            # Check if table exists
            if not catalog.table_exists(table, schema):
                print_error(f"Table '{schema}.{table}' does not exist")
                raise typer.Exit(1)

            # Get table information
            columns_data = catalog.describe_table(table, schema)
            indexes_data = catalog.list_indexes(table, schema)

            constraints_data = None
            fk_details = None
            if constraints:
                constraints_data = catalog.list_constraints(table, schema)
                fk_details = catalog.get_foreign_key_details(table, schema)

            if json_output:
                result = create_describe_result(
                    columns=columns_data,
                    indexes=indexes_data,
                    database=catalog.database_name,
                    schema=schema,
                    table=table,
                    show_constraints=constraints,
                    constraints=constraints_data,
                    foreign_key_details=fk_details
                )
                if output_file:
                    save_json_to_file(result, output_file)
                    print_success(f"Table description saved to {output_file}")
                else:
                    display_json(result)
            else:
                # Display table structure
                display_table(columns_data, f"Structure of '{schema}.{table}'")

                # Display indexes
                if indexes_data:
                    console.print("\n")
                    display_table(indexes_data, f"Indexes for '{schema}.{table}'")

                # Display constraints if requested
                if constraints and constraints_data:
                    console.print("\n")
                    display_constraints(constraints_data, fk_details or [], f"Constraints for '{schema}.{table}'")

    except DatabaseConnectionError as e:
        print_error(f"Connection failed: {e}")
        raise typer.Exit(1)
    except QueryExecutionError as e:
        print_error(f"Query failed: {e}")
        raise typer.Exit(1)

@app.command()
def info(
    connection_string: str = typer.Option(..., "--db", "-d", help="PostgreSQL connection string"),
    json_output: bool = typer.Option(False, "--json", "-j", help="Output results as JSON"),
    output_file: Optional[str] = typer.Option(None, "--output", "-o", help="Save output to file")
):
    """Show database connection information"""
    if not validate_connection_string(connection_string):
        print_error("Invalid connection string format. Expected: postgresql://user:password@host:port/database")
        raise typer.Exit(1)

    try:
        with PostgreSQLCatalog(connection_string) as catalog:
            db_info = catalog.get_database_info()

            if json_output:
                result = create_info_result(db_info, catalog.database_name)
                if output_file:
                    save_json_to_file(result, output_file)
                    print_success(f"Database info saved to {output_file}")
                else:
                    display_json(result)
            else:
                display_database_info(db_info)

    except DatabaseConnectionError as e:
        print_error(f"Connection failed: {e}")
        raise typer.Exit(1)
    except QueryExecutionError as e:
        print_error(f"Query failed: {e}")
        raise typer.Exit(1)

@app.command()
def interactive():
    """Interactive mode for exploring database catalog"""
    connection_string = typer.prompt("Enter PostgreSQL connection string")

    if not validate_connection_string(connection_string):
        print_error("Invalid connection string format. Expected: postgresql://user:password@host:port/database")
        raise typer.Exit(1)

    try:
        catalog = PostgreSQLCatalog(connection_string)
        catalog.connect()
    except DatabaseConnectionError as e:
        print_error(f"Connection failed: {e}")
        raise typer.Exit(1)

    print_success("Connected to PostgreSQL database!")
    console.print("Type 'help' for available commands or 'quit' to exit")

    try:
        _interactive_loop(catalog)
    finally:
        catalog.disconnect()
        print_success("Goodbye!")

def _interactive_loop(catalog: PostgreSQLCatalog) -> None:
    """Main interactive command loop."""
    json_mode = False  # Toggle for JSON output in interactive mode

    while True:
        try:
            command = typer.prompt("\npsql-catalog>", default="").strip()

            if command.lower() in ['quit', 'exit', 'q']:
                break
            elif command.lower() in ['help', 'h']:
                display_help()
            elif command.lower() == 'json':
                json_mode = not json_mode
                mode_str = "enabled" if json_mode else "disabled"
                print_success(f"JSON output mode {mode_str}")
            elif command.lower() == 'info':
                db_info = catalog.get_database_info()
                if json_mode:
                    result = create_info_result(db_info, catalog.database_name)
                    display_json(result)
                else:
                    display_database_info(db_info)
            elif command.lower() == 'schemas':
                schemas_data = catalog.list_schemas()
                if json_mode:
                    result = create_schemas_result(schemas_data, catalog.database_name)
                    display_json(result)
                else:
                    display_table(schemas_data, "Database Schemas")
            elif command.startswith('tables'):
                _handle_tables_command(catalog, command, json_mode)
            elif command.startswith('describe-all'):
                _handle_describe_all_command(catalog, command, json_mode)
            elif command.startswith('describe'):
                _handle_describe_command(catalog, command, json_mode)
            elif command.startswith('query'):
                _handle_query_command(catalog, command, json_mode)
            elif command:
                print_error(f"Unknown command: {command}")
                console.print("Type 'help' for available commands")

        except KeyboardInterrupt:
            print_warning("\nUse 'quit' to exit")

        except Exception as e:
            print_error(f"Error: {e}")

def _handle_tables_command(catalog: PostgreSQLCatalog, command: str, json_mode: bool = False) -> None:
    """Handle the 'tables' command in interactive mode."""
    parts = command.split()
    schema_name = parts[1] if len(parts) > 1 else 'public'

    try:
        if not catalog.schema_exists(schema_name):
            print_error(f"Schema '{schema_name}' does not exist")
            return

        tables_data = catalog.list_tables(schema_name)
        if json_mode:
            result = create_tables_result(tables_data, catalog.database_name, schema_name)
            display_json(result)
        else:
            display_table(tables_data, f"Tables in '{schema_name}' Schema")
    except QueryExecutionError as e:
        print_error(f"Failed to list tables: {e}")

def _handle_describe_command(catalog: PostgreSQLCatalog, command: str, json_mode: bool = False) -> None:
    """Handle the 'describe' command in interactive mode."""
    parts = command.split()
    if len(parts) < 2:
        print_error("Usage: describe <table> [schema] [--constraints]")
        return

    table_name = parts[1]
    schema_name = 'public'
    show_constraints = False

    # Parse additional parameters
    for i, part in enumerate(parts[2:], 2):
        if part.startswith('--'):
            if part in ['--constraints', '-c']:
                show_constraints = True
        else:
            schema_name = part

    try:
        if not catalog.table_exists(table_name, schema_name):
            print_error(f"Table '{schema_name}.{table_name}' does not exist")
            return

        # Get table information
        columns_data = catalog.describe_table(table_name, schema_name)
        indexes_data = catalog.list_indexes(table_name, schema_name)

        constraints_data = None
        fk_details = None
        if show_constraints:
            constraints_data = catalog.list_constraints(table_name, schema_name)
            fk_details = catalog.get_foreign_key_details(table_name, schema_name)

        if json_mode:
            result = create_describe_result(
                columns=columns_data,
                indexes=indexes_data,
                database=catalog.database_name,
                schema=schema_name,
                table=table_name,
                show_constraints=show_constraints,
                constraints=constraints_data,
                foreign_key_details=fk_details
            )
            display_json(result)
        else:
            # Display table structure
            display_table(columns_data, f"Structure of '{schema_name}.{table_name}'")

            # Display indexes
            if indexes_data:
                console.print("\n")
                display_table(indexes_data, f"Indexes for '{schema_name}.{table_name}'")

            # Display constraints if requested
            if show_constraints and constraints_data:
                console.print("\n")
                display_constraints(constraints_data, fk_details or [], f"Constraints for '{schema_name}.{table_name}'")

    except QueryExecutionError as e:
        print_error(f"Failed to describe table: {e}")

def _handle_query_command(catalog: PostgreSQLCatalog, command: str, json_mode: bool = False) -> None:
    """Handle the 'query' command in interactive mode."""
    sql_query = command[5:].strip()  # Remove 'query' prefix

    if not sql_query:
        print_error("Usage: query <sql>")
        return

    try:
        results = catalog.execute_query(sql_query)
        if results:
            if json_mode:
                result = create_query_result(sql_query, results, catalog.database_name)
                display_json(result)
            else:
                display_table(results, "Query Results")
        else:
            print_warning("Query executed successfully but returned no results")
    except QueryExecutionError as e:
        print_error(f"Query failed: {e}")

def main():
    """Main entry point"""
    try:
        app()
    except KeyboardInterrupt:
        print_warning("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print_error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
