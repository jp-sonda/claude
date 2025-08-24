"""
Display and formatting utilities for psql-catalog.
"""

import json
from typing import List, Dict, Any, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.syntax import Syntax

from .serialization import CatalogResult

console = Console()


def display_table(data: List[Dict[str, Any]], title: str) -> None:
    """
    Display data in a rich table format.

    Args:
        data: List of dictionaries containing the data to display
        title: Title for the table
    """
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


def display_json(result: CatalogResult, pretty: bool = True) -> None:
    """
    Display a catalog result as JSON.

    Args:
        result: Catalog result to display
        pretty: Whether to format the JSON with indentation
    """
    json_str = result.as_json(indent=2 if pretty else None)

    if pretty:
        # Use Rich syntax highlighting for pretty JSON
        syntax = Syntax(json_str, "json", theme="monokai", line_numbers=False)
        console.print(syntax)
    else:
        console.print(json_str)


def display_json_raw(data: List[Dict[str, Any]], title: str = "Data") -> None:
    """
    Display raw data as JSON (for simple cases).

    Args:
        data: List of dictionaries to display
        title: Title for the JSON output
    """
    output = {
        "title": title,
        "count": len(data),
        "data": data
    }

    json_str = json.dumps(output, indent=2, default=str)
    syntax = Syntax(json_str, "json", theme="monokai", line_numbers=False)
    console.print(syntax)


def display_table(data: List[Dict[str, Any]], title: str) -> None:
    """
    Display data in a rich table format.

    Args:
        data: List of dictionaries containing the data to display
        title: Title for the table
    """
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


def display_constraints(
    constraints_data: List[Dict[str, Any]],
    fk_details: List[Dict[str, Any]],
    title: str
) -> None:
    """
    Display constraints in a formatted way, grouped by constraint type.

    Args:
        constraints_data: List of constraint information
        fk_details: List of foreign key details
        title: Title for the constraints display
    """
    if not constraints_data:
        console.print(f"[yellow]No {title.lower()} found[/yellow]")
        return

    # Group constraints by type
    constraint_groups = {}
    for constraint in constraints_data:
        constraint_type = constraint['constraint_type']
        if constraint_type not in constraint_groups:
            constraint_groups[constraint_type] = []
        constraint_groups[constraint_type].append(constraint)

    # Display each type of constraint
    for constraint_type in ['PRIMARY KEY', 'FOREIGN KEY', 'UNIQUE', 'CHECK']:
        if constraint_type in constraint_groups:
            console.print(f"\n[bold cyan]{constraint_type} Constraints:[/bold cyan]")

            if constraint_type == 'FOREIGN KEY':
                _display_foreign_key_constraints(constraint_groups[constraint_type], fk_details)
            elif constraint_type == 'CHECK':
                _display_check_constraints(constraint_groups[constraint_type])
            else:
                _display_standard_constraints(constraint_groups[constraint_type])


def _display_foreign_key_constraints(constraints: List[Dict[str, Any]], fk_details: List[Dict[str, Any]]) -> None:
    """Display foreign key constraints with detailed information."""
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Constraint Name")
    table.add_column("Column")
    table.add_column("References")
    table.add_column("On Update")
    table.add_column("On Delete")
    table.add_column("Deferrable")

    # Create a lookup for FK details
    fk_lookup = {fk['constraint_name']: fk for fk in fk_details}

    processed_fks = set()
    for constraint in constraints:
        constraint_name = constraint['constraint_name']
        if constraint_name not in processed_fks:
            fk_detail = fk_lookup.get(constraint_name, {})

            references = ""
            if constraint['foreign_table_column']:
                references = constraint['foreign_table_column']
            elif fk_detail:
                references = f"{fk_detail.get('foreign_table_schema', '')}.{fk_detail.get('foreign_table_name', '')}.{fk_detail.get('foreign_column_name', '')}"

            table.add_row(
                constraint_name,
                constraint['column_name'] or "",
                references,
                fk_detail.get('on_update', 'N/A'),
                fk_detail.get('on_delete', 'N/A'),
                "Yes" if constraint.get('is_deferrable') == 'YES' else "No"
            )
            processed_fks.add(constraint_name)

    console.print(table)


def _display_check_constraints(constraints: List[Dict[str, Any]]) -> None:
    """Display check constraints with their conditions."""
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Constraint Name")
    table.add_column("Column")
    table.add_column("Check Clause")
    table.add_column("Deferrable")

    for constraint in constraints:
        table.add_row(
            constraint['constraint_name'],
            constraint['column_name'] or "",
            constraint['check_clause'] or "",
            "Yes" if constraint.get('is_deferrable') == 'YES' else "No"
        )

    console.print(table)


def _display_standard_constraints(constraints: List[Dict[str, Any]]) -> None:
    """Display standard constraints (PRIMARY KEY, UNIQUE)."""
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Constraint Name")
    table.add_column("Column")
    table.add_column("Deferrable")

    for constraint in constraints:
        table.add_row(
            constraint['constraint_name'],
            constraint['column_name'] or "",
            "Yes" if constraint.get('is_deferrable') == 'YES' else "No"
        )

    console.print(table)


def display_database_info(db_info: Dict[str, Any]) -> None:
    """
    Display database connection information.

    Args:
        db_info: Dictionary containing database information
    """
    if not db_info:
        return

    info_text = Text()
    info_text.append("Database: ", style="bold cyan")
    info_text.append(f"{db_info.get('database_name', 'Unknown')}\n")
    info_text.append("User: ", style="bold cyan")
    info_text.append(f"{db_info.get('current_user', 'Unknown')}\n")
    info_text.append("Encoding: ", style="bold cyan")
    info_text.append(f"{db_info.get('encoding', 'Unknown')}\n")
    info_text.append("Timezone: ", style="bold cyan")
    info_text.append(f"{db_info.get('timezone', 'Unknown')}")

    panel = Panel(info_text, title="[bold green]Database Information[/bold green]", expand=False)
    console.print(panel)


def print_success(message: str) -> None:
    """Print a success message in green."""
    console.print(f"[green]{message}[/green]")


def print_error(message: str) -> None:
    """Print an error message in red."""
    console.print(f"[red]{message}[/red]")


def print_warning(message: str) -> None:
    """Print a warning message in yellow."""
    console.print(f"[yellow]{message}[/yellow]")


def print_info(message: str) -> None:
    """Print an info message in blue."""
    console.print(f"[blue]{message}[/blue]")


def display_help() -> None:
    """Display help information for interactive mode."""
    help_text = """
Available commands:
- schemas: List all schemas
- tables [schema]: List tables in schema (default: public)
- describe <table> [schema] [--constraints]: Describe table structure
- query <sql>: Execute custom SQL query
- info: Show database connection information
- json: Toggle JSON output mode on/off
- help: Show this help
- quit: Exit interactive mode

Options for describe:
- --constraints or -c: Show integrity constraints (PK, FK, UNIQUE, CHECK)

JSON mode:
- Type 'json' to toggle JSON output format
- When JSON mode is enabled, all results will be displayed as formatted JSON
- JSON mode persists until toggled off

Examples:
- tables public
- describe users public --constraints
- query SELECT * FROM pg_tables LIMIT 5;
- json (to toggle JSON mode)
    """
    console.print(help_text)
