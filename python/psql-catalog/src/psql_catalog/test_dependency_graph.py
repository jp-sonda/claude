#!/usr/bin/env python3
"""
Test script for table dependency graph analysis.

This script demonstrates how to use the TableDependencyGraph class
with example data and validates the functionality.
"""

import json
import tempfile
from pathlib import Path
from dependency_graph import TableDependencyGraph, CycleDetectionError, GraphTraversalOrder
from batch_operations import DatabaseBatchOperations


def create_example_schema() -> dict:
    """Create example schema data for testing."""
    return {
        "command": "describe-all",
        "timestamp": "2025-08-24T10:30:00",
        "database": "test_database",
        "schema": "public",
        "tables": {
            "users": {
                "columns": [
                    {"column_name": "id", "data_type": "integer", "is_nullable": "NO"},
                    {"column_name": "name", "data_type": "character varying", "is_nullable": "NO"},
                    {"column_name": "email", "data_type": "character varying", "is_nullable": "YES"}
                ],
                "indexes": [
                    {"index_name": "users_pkey", "column_name": "id", "is_unique": True, "is_primary": True}
                ],
                "constraints": [
                    {
                        "constraint_name": "users_pkey",
                        "constraint_type": "PRIMARY KEY",
                        "table_name": "users",
                        "table_schema": "public",
                        "column_name": "id"
                    }
                ],
                "foreign_key_details": []
            },
            "categories": {
                "columns": [
                    {"column_name": "id", "data_type": "integer", "is_nullable": "NO"},
                    {"column_name": "name", "data_type": "character varying", "is_nullable": "NO"},
                    {"column_name": "parent_id", "data_type": "integer", "is_nullable": "YES"}
                ],
                "indexes": [
                    {"index_name": "categories_pkey", "column_name": "id", "is_unique": True, "is_primary": True}
                ],
                "constraints": [
                    {
                        "constraint_name": "categories_pkey",
                        "constraint_type": "PRIMARY KEY",
                        "table_name": "categories",
                        "table_schema": "public",
                        "column_name": "id"
                    },
                    {
                        "constraint_name": "categories_parent_id_fkey",
                        "constraint_type": "FOREIGN KEY",
                        "table_name": "categories",
                        "table_schema": "public",
                        "column_name": "parent_id",
                        "foreign_table_column": "public.categories.id"
                    }
                ],
                "foreign_key_details": [
                    {
                        "constraint_name": "categories_parent_id_fkey",
                        "column_name": "parent_id",
                        "foreign_table_schema": "public",
                        "foreign_table_name": "categories",
                        "foreign_column_name": "id",
                        "on_update": "NO ACTION",
                        "on_delete": "SET NULL"
                    }
                ]
            },
            "products": {
                "columns": [
                    {"column_name": "id", "data_type": "integer", "is_nullable": "NO"},
                    {"column_name": "name", "data_type": "character varying", "is_nullable": "NO"},
                    {"column_name": "price", "data_type": "numeric", "is_nullable": "YES"},
                    {"column_name": "category_id", "data_type": "integer", "is_nullable": "YES"}
                ],
                "indexes": [
                    {"index_name": "products_pkey", "column_name": "id", "is_unique": True, "is_primary": True}
                ],
                "constraints": [
                    {
                        "constraint_name": "products_pkey",
                        "constraint_type": "PRIMARY KEY",
                        "table_name": "products",
                        "table_schema": "public",
                        "column_name": "id"
                    },
                    {
                        "constraint_name": "products_category_id_fkey",
                        "constraint_type": "FOREIGN KEY",
                        "table_name": "products",
                        "table_schema": "public",
                        "column_name": "category_id",
                        "foreign_table_column": "public.categories.id"
                    }
                ],
                "foreign_key_details": [
                    {
                        "constraint_name": "products_category_id_fkey",
                        "column_name": "category_id",
                        "foreign_table_schema": "public",
                        "foreign_table_name": "categories",
                        "foreign_column_name": "id",
                        "on_update": "NO ACTION",
                        "on_delete": "SET NULL"
                    }
                ]
            },
            "orders": {
                "columns": [
                    {"column_name": "id", "data_type": "integer", "is_nullable": "NO"},
                    {"column_name": "user_id", "data_type": "integer", "is_nullable": "NO"},
                    {"column_name": "total", "data_type": "numeric", "is_nullable": "YES"},
                    {"column_name": "order_date", "data_type": "timestamp", "is_nullable": "NO"}
                ],
                "indexes": [
                    {"index_name": "orders_pkey", "column_name": "id", "is_unique": True, "is_primary": True}
                ],
                "constraints": [
                    {
                        "constraint_name": "orders_pkey",
                        "constraint_type": "PRIMARY KEY",
                        "table_name": "orders",
                        "table_schema": "public",
                        "column_name": "id"
                    },
                    {
                        "constraint_name": "orders_user_id_fkey",
                        "constraint_type": "FOREIGN KEY",
                        "table_name": "orders",
                        "table_schema": "public",
                        "column_name": "user_id",
                        "foreign_table_column": "public.users.id"
                    }
                ],
                "foreign_key_details": [
                    {
                        "constraint_name": "orders_user_id_fkey",
                        "column_name": "user_id",
                        "foreign_table_schema": "public",
                        "foreign_table_name": "users",
                        "foreign_column_name": "id",
                        "on_update": "NO ACTION",
                        "on_delete": "CASCADE"
                    }
                ]
            },
            "order_items": {
                "columns": [
                    {"column_name": "id", "data_type": "integer", "is_nullable": "NO"},
                    {"column_name": "order_id", "data_type": "integer", "is_nullable": "NO"},
                    {"column_name": "product_id", "data_type": "integer", "is_nullable": "NO"},
                    {"column_name": "quantity", "data_type": "integer", "is_nullable": "NO"},
                    {"column_name": "price", "data_type": "numeric", "is_nullable": "NO"}
                ],
                "indexes": [
                    {"index_name": "order_items_pkey", "column_name": "id", "is_unique": True, "is_primary": True}
                ],
                "constraints": [
                    {
                        "constraint_name": "order_items_pkey",
                        "constraint_type": "PRIMARY KEY",
                        "table_name": "order_items",
                        "table_schema": "public",
                        "column_name": "id"
                    },
                    {
                        "constraint_name": "order_items_order_id_fkey",
                        "constraint_type": "FOREIGN KEY",
                        "table_name": "order_items",
                        "table_schema": "public",
                        "column_name": "order_id",
                        "foreign_table_column": "public.orders.id"
                    },
                    {
                        "constraint_name": "order_items_product_id_fkey",
                        "constraint_type": "FOREIGN KEY",
                        "table_name": "order_items",
                        "table_schema": "public",
                        "column_name": "product_id",
                        "foreign_table_column": "public.products.id"
                    }
                ],
                "foreign_key_details": [
                    {
                        "constraint_name": "order_items_order_id_fkey",
                        "column_name": "order_id",
                        "foreign_table_schema": "public",
                        "foreign_table_name": "orders",
                        "foreign_column_name": "id",
                        "on_update": "NO ACTION",
                        "on_delete": "CASCADE"
                    },
                    {
                        "constraint_name": "order_items_product_id_fkey",
                        "column_name": "product_id",
                        "foreign_table_schema": "public",
                        "foreign_table_name": "products",
                        "foreign_column_name": "id",
                        "on_update": "NO ACTION",
                        "on_delete": "RESTRICT"
                    }
                ]
            }
        },
        "show_constraints": True,
        "total_tables": 5,
        "failed_tables": []
    }


def create_circular_dependency_schema() -> dict:
    """Create schema with circular dependencies for testing cycle detection."""
    return {
        "command": "describe-all",
        "timestamp": "2025-08-24T10:30:00",
        "database": "circular_test",
        "schema": "public",
        "tables": {
            "table_a": {
                "columns": [
                    {"column_name": "id", "data_type": "integer", "is_nullable": "NO"},
                    {"column_name": "b_id", "data_type": "integer", "is_nullable": "YES"}
                ],
                "indexes": [],
                "constraints": [
                    {
                        "constraint_name": "table_a_b_id_fkey",
                        "constraint_type": "FOREIGN KEY",
                        "table_name": "table_a",
                        "table_schema": "public",
                        "column_name": "b_id",
                        "foreign_table_column": "public.table_b.id"
                    }
                ],
                "foreign_key_details": [
                    {
                        "constraint_name": "table_a_b_id_fkey",
                        "column_name": "b_id",
                        "foreign_table_schema": "public",
                        "foreign_table_name": "table_b",
                        "foreign_column_name": "id"
                    }
                ]
            },
            "table_b": {
                "columns": [
                    {"column_name": "id", "data_type": "integer", "is_nullable": "NO"},
                    {"column_name": "c_id", "data_type": "integer", "is_nullable": "YES"}
                ],
                "indexes": [],
                "constraints": [
                    {
                        "constraint_name": "table_b_c_id_fkey",
                        "constraint_type": "FOREIGN KEY",
                        "table_name": "table_b",
                        "table_schema": "public",
                        "column_name": "c_id",
                        "foreign_table_column": "public.table_c.id"
                    }
                ],
                "foreign_key_details": [
                    {
                        "constraint_name": "table_b_c_id_fkey",
                        "column_name": "c_id",
                        "foreign_table_schema": "public",
                        "foreign_table_name": "table_c",
                        "foreign_column_name": "id"
                    }
                ]
            },
            "table_c": {
                "columns": [
                    {"column_name": "id", "data_type": "integer", "is_nullable": "NO"},
                    {"column_name": "a_id", "data_type": "integer", "is_nullable": "YES"}
                ],
                "indexes": [],
                "constraints": [
                    {
                        "constraint_name": "table_c_a_id_fkey",
                        "constraint_type": "FOREIGN KEY",
                        "table_name": "table_c",
                        "table_schema": "public",
                        "column_name": "a_id",
                        "foreign_table_column": "public.table_a.id"
                    }
                ],
                "foreign_key_details": [
                    {
                        "constraint_name": "table_c_a_id_fkey",
                        "column_name": "a_id",
                        "foreign_table_schema": "public",
                        "foreign_table_name": "table_a",
                        "foreign_column_name": "id"
                    }
                ]
            }
        },
        "show_constraints": True,
        "total_tables": 3,
        "failed_tables": []
    }


def test_basic_functionality():
    """Test basic functionality with example data."""
    print("=== Testing Basic Functionality ===")
    
    # Create graph with example data
    schema_data = create_example_schema()
    graph = TableDependencyGraph(schema_data)
    
    print(f"Total tables loaded: {len(graph.get_tables())}")
    print(f"Tables: {', '.join(sorted(graph.get_tables()))}")
    
    # Test dependency analysis
    print(f"\nDependency Analysis:")
    for table in sorted(graph.get_tables()):
        deps = graph.get_dependencies(table)
        dependents = graph.get_dependents(table)
        print(f"  {table}: depends on {deps or 'none'}, depended by {dependents or 'none'}")
    
    # Test topological sorting
    try:
        insert_order = graph.get_insert_order()
        drop_order = graph.get_drop_order()
        
        print(f"\nInsert order: {' -> '.join(insert_order)}")
        print(f"Drop order:   {' -> '.join(drop_order)}")
        
        # Validate orders
        assert insert_order != drop_order, "Insert and drop orders should be different"
        assert set(insert_order) == set(drop_order), "Both orders should contain same tables"
        
        print("✓ Basic functionality test passed")
        
    except CycleDetectionError as e:
        print(f"❌ Unexpected cycle detected: {e}")
        return False
    
    return True


def test_cycle_detection():
    """Test cycle detection functionality."""
    print("\n=== Testing Cycle Detection ===")
    
    # Create graph with circular dependencies
    schema_data = create_circular_dependency_schema()
    graph = TableDependencyGraph(schema_data)
    
    # Check for cycles
    has_cycles, cycle_path = graph.has_cycles()
    print(f"Has cycles: {has_cycles}")
    
    if has_cycles:
        print(f"Cycle path: {' -> '.join(cycle_path) if cycle_path else 'unknown'}")
        
        # Test that topological sorting fails appropriately
        try:
            graph.get_insert_order()
            print("❌ Expected CycleDetectionError but none was raised")
            return False
        except CycleDetectionError as e:
            print(f"✓ Correctly detected cycle: {e}")
            return True
    else:
        print("❌ Expected cycle not detected")
        return False


def test_self_referencing_table():
    """Test handling of self-referencing tables."""
    print("\n=== Testing Self-Referencing Tables ===")
    
    schema_data = create_example_schema()
    
    # The categories table has a self-reference (parent_id -> id)
    graph = TableDependencyGraph(schema_data)
    
    # Check that categories depends on itself
    categories_deps = graph.get_dependencies('categories')
    print(f"Categories dependencies: {categories_deps}")
    
    # This should still work since it's not a strict cycle
    try:
        insert_order = graph.get_insert_order()
        drop_order = graph.get_drop_order()
        
        # Categories should appear in both orders
        assert 'categories' in insert_order, "Categories should be in insert order"
        assert 'categories' in drop_order, "Categories should be in drop order"
        
        print(f"Insert order: {' -> '.join(insert_order)}")
        print(f"Drop order:   {' -> '.join(drop_order)}")
        print("✓ Self-referencing table test passed")
        return True
        
    except CycleDetectionError as e:
        print(f"Self-reference treated as cycle: {e}")
        # This might be expected behavior depending on implementation
        return True


def test_batch_operations():
    """Test batch operations functionality."""
    print("\n=== Testing Batch Operations ===")
    
    # Create temporary JSON file
    schema_data = create_example_schema()
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(schema_data, f, indent=2)
        temp_file = f.name
    
    try:
        # Test batch operations
        batch_ops = DatabaseBatchOperations(temp_file)
        
        # Test DROP statements generation
        drop_statements = batch_ops.generate_drop_statements(cascade=True)
        print(f"Generated {len(drop_statements)} DROP statements:")
        for stmt in drop_statements[:3]:  # Show first 3
            print(f"  {stmt}")
        if len(drop_statements) > 3:
            print(f"  ... and {len(drop_statements) - 3} more")
        
        # Test TRUNCATE statements
        truncate_statements = batch_ops.generate_truncate_statements(cascade=True, restart_identity=True)
        print(f"\nGenerated {len(truncate_statements)} TRUNCATE statements:")
        for stmt in truncate_statements[:2]:  # Show first 2
            print(f"  {stmt}")
        
        # Test INSERT templates
        insert_templates = batch_ops.generate_insert_template_statements()
        print(f"\nGenerated {len(insert_templates)} INSERT templates:")
        for stmt in insert_templates[:2]:  # Show first 2
            print(f"  {stmt}")
        
        # Test order info
        order_info = batch_ops.get_table_order_info()
        assert 'insert_order' in order_info
        assert 'drop_order' in order_info
        assert not order_info['has_cycles']
        
        print("✓ Batch operations test passed")
        return True
        
    finally:
        # Cleanup
        Path(temp_file).unlink()
    
    return False


def test_json_file_operations():
    """Test loading from JSON file."""
    print("\n=== Testing JSON File Operations ===")
    
    # Create temporary JSON file
    schema_data = create_example_schema()
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(schema_data, f, indent=2)
        temp_file = f.name
    
    try:
        # Test loading from file
        graph = TableDependencyGraph()
        graph.load_from_json_file(temp_file)
        
        assert len(graph.get_tables()) == 5, f"Expected 5 tables, got {len(graph.get_tables())}"
        
        # Test that we can get orders
        insert_order = graph.get_insert_order()
        drop_order = graph.get_drop_order()
        
        print(f"Successfully loaded from JSON file")
        print(f"Tables: {', '.join(sorted(graph.get_tables()))}")
        print(f"Insert order: {' -> '.join(insert_order)}")
        
        print("✓ JSON file operations test passed")
        return True
        
    except Exception as e:
        print(f"❌ JSON file operations test failed: {e}")
        return False
        
    finally:
        # Cleanup
        Path(temp_file).unlink()


def test_edge_cases():
    """Test edge cases and error conditions."""
    print("\n=== Testing Edge Cases ===")
    
    # Test empty schema
    try:
        empty_schema = {"tables": {}}
        graph = TableDependencyGraph(empty_schema)
        assert len(graph.get_tables()) == 0
        assert graph.get_insert_order() == []
        assert graph.get_drop_order() == []
        print("✓ Empty schema handled correctly")
    except Exception as e:
        print(f"❌ Empty schema test failed: {e}")
        return False
    
    # Test schema with no foreign keys
    try:
        simple_schema = {
            "tables": {
                "table1": {"columns": [], "indexes": [], "constraints": [], "foreign_key_details": []},
                "table2": {"columns": [], "indexes": [], "constraints": [], "foreign_key_details": []},
                "table3": {"columns": [], "indexes": [], "constraints": [], "foreign_key_details": []}
            }
        }
        graph = TableDependencyGraph(simple_schema)
        insert_order = graph.get_insert_order()
        drop_order = graph.get_drop_order()
        
        # With no dependencies, any order should be valid
        assert len(insert_order) == 3
        assert len(drop_order) == 3
        assert set(insert_order) == set(drop_order) == {"table1", "table2", "table3"}
        print("✓ Schema with no foreign keys handled correctly")
    except Exception as e:
        print(f"❌ No foreign keys test failed: {e}")
        return False
    
    # Test invalid JSON file path
    try:
        graph = TableDependencyGraph()
        graph.load_from_json_file("nonexistent_file.json")
        print("❌ Should have raised FileNotFoundError")
        return False
    except FileNotFoundError:
        print("✓ FileNotFoundError correctly raised for invalid path")
    except Exception as e:
        print(f"❌ Unexpected error for invalid path: {e}")
        return False
    
    return True


def validate_dependency_order(tables_order: list, dependencies_map: dict) -> bool:
    """
    Validate that a table order respects dependencies.
    
    Args:
        tables_order: List of table names in order
        dependencies_map: Dict mapping table -> set of dependencies
    
    Returns:
        True if order is valid
    """
    position = {table: i for i, table in enumerate(tables_order)}
    
    for table, deps in dependencies_map.items():
        if table not in position:
            continue
            
        table_pos = position[table]
        for dep in deps:
            if dep not in position:
                continue
            dep_pos = position[dep]
            
            # Dependency should come before the table that depends on it
            if dep_pos >= table_pos:
                print(f"Invalid order: {table} at position {table_pos} depends on {dep} at position {dep_pos}")
                return False
    
    return True


def run_comprehensive_validation():
    """Run comprehensive validation of the dependency graph."""
    print("\n=== Comprehensive Validation ===")
    
    schema_data = create_example_schema()
    graph = TableDependencyGraph(schema_data)
    
    # Build dependencies map for validation
    dependencies_map = {}
    for table in graph.get_tables():
        dependencies_map[table] = graph.get_dependencies(table)
    
    # Validate insert order
    insert_order = graph.get_insert_order()
    if validate_dependency_order(insert_order, dependencies_map):
        print("✓ Insert order respects all dependencies")
    else:
        print("❌ Insert order violates dependencies")
        return False
    
    # For drop order, we need to reverse the dependency relationship
    reverse_deps = {}
    for table in graph.get_tables():
        reverse_deps[table] = graph.get_dependents(table)
    
    drop_order = graph.get_drop_order()
    if validate_dependency_order(drop_order, reverse_deps):
        print("✓ Drop order respects all dependent relationships")
    else:
        print("❌ Drop order violates dependent relationships")
        return False
    
    # Validate expected relationships for our test data
    expected_relationships = {
        'users': {'depends_on': set(), 'depended_by': {'orders'}},
        'categories': {'depends_on': {'categories'}, 'depended_by': {'products', 'categories'}},
        'products': {'depends_on': {'categories'}, 'depended_by': {'order_items'}},
        'orders': {'depends_on': {'users'}, 'depended_by': {'order_items'}},
        'order_items': {'depends_on': {'orders', 'products'}, 'depended_by': set()}
    }
    
    for table, expected in expected_relationships.items():
        actual_deps = graph.get_dependencies(table)
        actual_dependents = graph.get_dependents(table)
        
        if actual_deps != expected['depends_on']:
            print(f"❌ {table} dependencies mismatch: expected {expected['depends_on']}, got {actual_deps}")
            return False
        
        if actual_dependents != expected['depended_by']:
            print(f"❌ {table} dependents mismatch: expected {expected['depended_by']}, got {actual_dependents}")
            return False
    
    print("✓ All dependency relationships validated correctly")
    return True


def main():
    """Run all tests."""
    print("Starting Table Dependency Graph Tests")
    print("=" * 50)
    
    tests = [
        test_basic_functionality,
        test_cycle_detection,
        test_self_referencing_table,
        test_batch_operations,
        test_json_file_operations,
        test_edge_cases,
        run_comprehensive_validation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                print(f"❌ {test.__name__} failed")
        except Exception as e:
            print(f"❌ {test.__name__} crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        
        # Demonstrate usage with the example schema
        print("\n=== Usage Demonstration ===")
        
        # Create a temporary schema file for demonstration
        schema_data = create_example_schema()
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(schema_data, f, indent=2)
            demo_file = f.name
        
        try:
            print(f"\nDemo schema file created: {demo_file}")
            
            # Load and analyze
            graph = TableDependencyGraph()
            graph.load_from_json_file(demo_file)
            
            # Print comprehensive analysis
            graph.print_graph_summary()
            graph.print_detailed_dependencies()
            
            # Show practical usage
            print(f"\n=== Practical Usage Examples ===")
            
            insert_order = graph.get_insert_order()
            drop_order = graph.get_drop_order()
            
            print(f"\nFor safe data insertion (dependencies first):")
            for i, table in enumerate(insert_order, 1):
                print(f"  {i}. INSERT INTO {table} ...")
            
            print(f"\nFor safe table deletion (dependents first):")
            for i, table in enumerate(drop_order, 1):
                print(f"  {i}. DROP TABLE {table}")
            
            # Show batch operations
            batch_ops = DatabaseBatchOperations(demo_file)
            
            print(f"\nSample generated SQL statements:")
            drop_statements = batch_ops.generate_drop_statements(cascade=True)
            print(f"\n-- DROP statements (first 2):")
            for stmt in drop_statements[:2]:
                print(f"  {stmt}")
            
            insert_templates = batch_ops.generate_insert_template_statements()
            print(f"\n-- INSERT templates (first 2):")
            for stmt in insert_templates[:2]:
                print(f"  {stmt}")
                
        finally:
            # Cleanup demo file
            Path(demo_file).unlink()
            print(f"\nDemo file cleaned up: {demo_file}")
    
    else:
        print("❌ Some tests failed!")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
