#!/usr/bin/env python3
"""
Batch database operations using table dependency analysis.

This script provides utilities for performing batch operations on database tables
in the correct order based on their foreign key dependencies.
"""

import argparse
import json
import sys
from typing import List, Optional, Dict, Any
from pathlib import Path

# Assuming the dependency_graph module is in the same package
from dependency_graph import TableDependencyGraph, CycleDetectionError, analyze_schema_file


class BatchOperationError(Exception):
    """Raised when batch operation fails."""
    pass


class DatabaseBatchOperations:
    """
    Utility class for performing batch database operations in dependency order.
    """
    
    def __init__(self, schema_json_path: str, connection_string: Optional[str] = None):
        """
        Initialize batch operations handler.
        
        Args:
            schema_json_path: Path to the schema JSON file from psql-catalog
            connection_string: Optional PostgreSQL connection string for direct execution
        """
        self.schema_json_path = Path(schema_json_path)
        self.connection_string = connection_string
        self.dependency_graph = analyze_schema_file(str(self.schema_json_path))
        
    def generate_drop_statements(self, cascade: bool = False) -> List[str]:
        """
        Generate DROP TABLE statements in safe order.
        
        Args:
            cascade: Whether to use CASCADE option
            
        Returns:
            List of SQL DROP statements
        """
        try:
            drop_order = self.dependency_graph.get_drop_order()
            cascade_clause = " CASCADE" if cascade else ""
            
            statements = []
            for table in drop_order:
                statements.append(f"DROP TABLE IF EXISTS {table}{cascade_clause};")
            
            return statements
            
        except CycleDetectionError as e:
            raise BatchOperationError(f"Cannot generate DROP statements due to circular dependencies: {e}")
    
    def generate_truncate_statements(self, cascade: bool = False, restart_identity: bool = False) -> List[str]:
        """
        Generate TRUNCATE statements in safe order.
        
        Args:
            cascade: Whether to use CASCADE option
            restart_identity: Whether to restart identity sequences
            
        Returns:
            List of SQL TRUNCATE statements
        """
        try:
            drop_order = self.dependency_graph.get_drop_order()  # Same order as DROP
            
            options = []
            if restart_identity:
                options.append("RESTART IDENTITY")
            if cascade:
                options.append("CASCADE")
            
            options_clause = " " + " ".join(options) if options else ""
            
            statements = []
            for table in drop_order:
                statements.append(f"TRUNCATE TABLE {table}{options_clause};")
            
            return statements
            
        except CycleDetectionError as e:
            raise BatchOperationError(f"Cannot generate TRUNCATE statements due to circular dependencies: {e}")
    
    def generate_disable_constraints_statements(self, constraint_type: str = "FOREIGN KEY") -> List[str]:
        """
        Generate statements to disable constraints in all tables.
        
        Args:
            constraint_type: Type of constraint to disable (default: FOREIGN KEY)
            
        Returns:
            List of SQL statements to disable constraints
        """
        tables = self.dependency_graph.get_tables()
        statements = []
        
        # For foreign keys, we can disable all at once
        if constraint_type.upper() == "FOREIGN KEY":
            for table in tables:
                # This is PostgreSQL specific - disable all FK constraints on table
                statements.append(f"ALTER TABLE {table} DISABLE TRIGGER ALL;")
        
        return statements
    
    def generate_enable_constraints_statements(self, constraint_type: str = "FOREIGN KEY") -> List[str]:
        """
        Generate statements to re-enable constraints in all tables.
        
        Args:
            constraint_type: Type of constraint to enable (default: FOREIGN KEY)
            
        Returns:
            List of SQL statements to enable constraints
        """
        tables = self.dependency_graph.get_tables()
        statements = []
        
        # For foreign keys, enable in dependency order
        if constraint_type.upper() == "FOREIGN KEY":
            insert_order = self.dependency_graph.get_insert_order()
            for table in insert_order:
                statements.append(f"ALTER TABLE {table} ENABLE TRIGGER ALL;")
        
        return statements
    
    def generate_insert_template_statements(self, include_columns: bool = True) -> List[str]:
        """
        Generate INSERT statement templates in safe order.
        
        Args:
            include_columns: Whether to include column names in INSERT statements
            
        Returns:
            List of INSERT statement templates
        """
        try:
            insert_order = self.dependency_graph.get_insert_order()
            statements = []
            
            # Load table structure from schema JSON
            with open(self.schema_json_path, 'r', encoding='utf-8') as f:
                schema_data = json.load(f)
            
            tables = schema_data.get('tables', {})
            
            for table in insert_order:
                if table in tables and 'columns' in tables[table]:
                    columns = tables[table]['columns']
                    if include_columns:
                        column_names = [col['column_name'] for col in columns]
                        columns_clause = f"({', '.join(column_names)})"
                        placeholders = ', '.join(['%s'] * len(column_names))
                        statements.append(f"INSERT INTO {table} {columns_clause} VALUES ({placeholders});")
                    else:
                        placeholders = ', '.join(['%s'] * len(columns))
                        statements.append(f"INSERT INTO {table} VALUES ({placeholders});")
                else:
                    # Fallback if no column info available
                    statements.append(f"INSERT INTO {table} VALUES (...);")
            
            return statements
            
        except CycleDetectionError as e:
            raise BatchOperationError(f"Cannot generate INSERT statements due to circular dependencies: {e}")
    
    def get_table_order_info(self) -> Dict[str, Any]:
        """
        Get comprehensive information about table ordering.
        
        Returns:
            Dictionary with ordering information
        """
        try:
            return {
                'insert_order': self.dependency_graph.get_insert_order(),
                'drop_order': self.dependency_graph.get_drop_order(),
                'dependency_info': self.dependency_graph.get_dependency_info(),
                'total_tables': len(self.dependency_graph.get_tables()),
                'has_cycles': self.dependency_graph.has_cycles()[0]
            }
        except CycleDetectionError as e:
            return {
                'error': str(e),
                'has_cycles': True
            }
    
    def save_sql_script(self, operation: str, output_file: str, **kwargs) -> None:
        """
        Save SQL statements to a file.
        
        Args:
            operation: Type of operation ('drop', 'truncate', 'insert_template')
            output_file: Path to output SQL file
            **kwargs: Additional options for the operation
        """
        statements = []
        
        if operation.lower() == 'drop':
            statements = self.generate_drop_statements(cascade=kwargs.get('cascade', False))
        elif operation.lower() == 'truncate':
            statements = self.generate_truncate_statements(
                cascade=kwargs.get('cascade', False),
                restart_identity=kwargs.get('restart_identity', False)
            )
        elif operation.lower() == 'insert_template':
            statements = self.generate_insert_template_statements(
                include_columns=kwargs.get('include_columns', True)
            )
        elif operation.lower() == 'disable_fk':
            statements = self.generate_disable_constraints_statements()
        elif operation.lower() == 'enable_fk':
            statements = self.generate_enable_constraints_statements()
        else:
            raise BatchOperationError(f"Unknown operation: {operation}")
        
        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"-- Generated {operation.upper()} statements\n")
            f.write(f"-- Based on schema analysis from: {self.schema_json_path}\n")
            f.write(f"-- Generated on: {self.dependency_graph.get_tables()}\n\n")
            
            if operation.lower() in ['drop', 'truncate']:
                f.write("-- Order: dependencies last (safe for deletion)\n")
            elif operation.lower() == 'insert_template':
                f.write("-- Order: dependencies first (safe for insertion)\n")
            
            f.write(f"-- Total statements: {len(statements)}\n\n")
            
            for i, stmt in enumerate(statements, 1):
                f.write(f"-- Statement {i}\n{stmt}\n\n")
    
    def execute_statements(self, statements: List[str], dry_run: bool = True) -> None:
        """
        Execute SQL statements (requires psycopg2 and connection string).
        
        Args:
            statements: List of SQL statements to execute
            dry_run: If True, only print statements without executing
        """
        if dry_run:
            print("DRY RUN - The following statements would be executed:")
            print("-" * 60)
            for i, stmt in enumerate(statements, 1):
                print(f"{i:2d}. {stmt}")
            print("-" * 60)
            return
        
        if not self.connection_string:
            raise BatchOperationError("Connection string required for statement execution")
        
        try:
            import psycopg2
            
            with psycopg2.connect(self.connection_string) as conn:
                with conn.cursor() as cursor:
                    for i, stmt in enumerate(statements, 1):
                        try:
                            print(f"Executing statement {i}: {stmt.strip()}")
                            cursor.execute(stmt)
                            print(f"✓ Statement {i} executed successfully")
                        except Exception as e:
                            print(f"❌ Statement {i} failed: {e}")
                            raise
                    
                    conn.commit()
                    print(f"\n✓ All {len(statements)} statements executed successfully")
                    
        except ImportError:
            raise BatchOperationError("psycopg2 is required for direct statement execution")
        except Exception as e:
            raise BatchOperationError(f"Failed to execute statements: {e}")


def main():
    """Command-line interface for batch operations."""
    parser = argparse.ArgumentParser(
        description="Perform batch database operations in dependency order",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze dependencies and show table order
  python batch_operations.py analyze my_schema.json
  
  # Generate DROP statements
  python batch_operations.py drop my_schema.json --output drop_tables.sql --cascade
  
  # Generate TRUNCATE statements
  python batch_operations.py truncate my_schema.json --output truncate_tables.sql
  
  # Generate INSERT templates
  python batch_operations.py insert-template my_schema.json --output insert_templates.sql
  
  # Show just the table orders
  python batch_operations.py order my_schema.json
        """
    )
    
    parser.add_argument('command', choices=['analyze', 'drop', 'truncate', 'insert-template', 'order'],
                       help='Operation to perform')
    parser.add_argument('schema_file', help='Path to schema JSON file from psql-catalog')
    parser.add_argument('--output', '-o', help='Output SQL file path')
    parser.add_argument('--cascade', action='store_true', 
                       help='Use CASCADE option (for DROP/TRUNCATE)')
    parser.add_argument('--restart-identity', action='store_true',
                       help='Use RESTART IDENTITY (for TRUNCATE)')
    parser.add_argument('--no-columns', action='store_true',
                       help='Omit column names from INSERT templates')
    parser.add_argument('--connection', '-c', help='PostgreSQL connection string for execution')
    parser.add_argument('--execute', action='store_true', 
                       help='Execute statements directly (requires --connection)')
    parser.add_argument('--dry-run', action='store_true', default=True,
                       help='Show statements without executing (default)')
    
    args = parser.parse_args()
    
    # Validate arguments
    if not Path(args.schema_file).exists():
        print(f"Error: Schema file '{args.schema_file}' not found", file=sys.stderr)
        sys.exit(1)
    
    if args.execute and not args.connection:
        print("Error: --connection required when using --execute", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Initialize batch operations handler
        batch_ops = DatabaseBatchOperations(args.schema_file, args.connection)
        
        if args.command == 'analyze':
            # Full analysis
            print(f"Analyzing schema file: {args.schema_file}")
            batch_ops.dependency_graph.print_graph_summary()
            batch_ops.dependency_graph.print_detailed_dependencies()
            
            # Show ordering information
            order_info = batch_ops.get_table_order_info()
            if 'error' not in order_info:
                print(f"\nRecommended Operation Orders:")
                print("-" * 40)
                print(f"INSERT order: {' -> '.join(order_info['insert_order'])}")
                print(f"DROP order:   {' -> '.join(order_info['drop_order'])}")
        
        elif args.command == 'order':
            # Just show the orders
            order_info = batch_ops.get_table_order_info()
            if 'error' in order_info:
                print(f"Error: {order_info['error']}", file=sys.stderr)
                sys.exit(1)
            
            print("Table Operation Orders:")
            print("-" * 25)
            print(f"INSERT: {' -> '.join(order_info['insert_order'])}")
            print(f"DROP:   {' -> '.join(order_info['drop_order'])}")
        
        elif args.command == 'drop':
            statements = batch_ops.generate_drop_statements(cascade=args.cascade)
            
            if args.output:
                batch_ops.save_sql_script('drop', args.output, cascade=args.cascade)
                print(f"DROP statements saved to: {args.output}")
            
            if args.execute:
                batch_ops.execute_statements(statements, dry_run=args.dry_run)
            else:
                print("Generated DROP statements:")
                for stmt in statements:
                    print(f"  {stmt}")
        
        elif args.command == 'truncate':
            statements = batch_ops.generate_truncate_statements(
                cascade=args.cascade,
                restart_identity=args.restart_identity
            )
            
            if args.output:
                batch_ops.save_sql_script('truncate', args.output, 
                                        cascade=args.cascade,
                                        restart_identity=args.restart_identity)
                print(f"TRUNCATE statements saved to: {args.output}")
            
            if args.execute:
                batch_ops.execute_statements(statements, dry_run=args.dry_run)
            else:
                print("Generated TRUNCATE statements:")
                for stmt in statements:
                    print(f"  {stmt}")
        
        elif args.command == 'insert-template':
            statements = batch_ops.generate_insert_template_statements(
                include_columns=not args.no_columns
            )
            
            if args.output:
                batch_ops.save_sql_script('insert_template', args.output,
                                        include_columns=not args.no_columns)
                print(f"INSERT templates saved to: {args.output}")
            else:
                print("Generated INSERT templates:")
                for stmt in statements:
                    print(f"  {stmt}")
    
    except (BatchOperationError, CycleDetectionError, FileNotFoundError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
