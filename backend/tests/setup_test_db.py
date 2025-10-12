"""
Test Database Setup Script
Creates and initializes the test database with schema
"""
import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Test database configuration
TEST_DB_CONFIG = {
    "host": os.getenv("TEST_DB_HOST", "localhost"),
    "port": int(os.getenv("TEST_DB_PORT", "5432")),
    "database": os.getenv("TEST_DB_NAME", "ghg_platform_test"),
    "user": os.getenv("TEST_DB_USER", "ghg_user"),
    "password": os.getenv("TEST_DB_PASSWORD", "1234"),
}

# Admin database configuration (for creating test database)
ADMIN_DB_CONFIG = {
    "host": TEST_DB_CONFIG["host"],
    "port": TEST_DB_CONFIG["port"],
    "database": "postgres",  # Connect to default postgres database
    "user": TEST_DB_CONFIG["user"],
    "password": TEST_DB_CONFIG["password"],
}


def create_test_database():
    """
    Create the test database if it doesn't exist
    """
    print(f"Creating test database: {TEST_DB_CONFIG['database']}")
    
    # Connect to postgres database to create test database
    conn = psycopg2.connect(**ADMIN_DB_CONFIG)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    
    # Check if database exists
    cursor.execute(
        "SELECT 1 FROM pg_database WHERE datname = %s",
        (TEST_DB_CONFIG["database"],)
    )
    exists = cursor.fetchone()
    
    if exists:
        print(f"Test database '{TEST_DB_CONFIG['database']}' already exists")
        # Drop and recreate for clean state
        print("Dropping existing test database...")
        cursor.execute(f"DROP DATABASE {TEST_DB_CONFIG['database']}")
    
    # Create the test database
    cursor.execute(f"CREATE DATABASE {TEST_DB_CONFIG['database']}")
    print(f"Test database '{TEST_DB_CONFIG['database']}' created successfully")
    
    cursor.close()
    conn.close()


def initialize_test_schema():
    """
    Initialize the test database schema using init.sql
    """
    print("Initializing test database schema...")
    
    # Read the schema SQL file
    schema_file = os.path.join(
        os.path.dirname(__file__), 
        '..', 
        '..', 
        'init.sql'
    )
    
    if not os.path.exists(schema_file):
        raise FileNotFoundError(f"Schema file not found: {schema_file}")
    
    with open(schema_file, 'r') as f:
        schema_sql = f.read()
    
    # Connect to test database and execute schema
    conn = psycopg2.connect(**TEST_DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        cursor.execute(schema_sql)
        conn.commit()
        print("Test database schema initialized successfully")
    except Exception as e:
        conn.rollback()
        print(f"Error initializing schema: {e}")
        raise
    finally:
        cursor.close()
        conn.close()


def verify_test_database():
    """
    Verify that the test database is set up correctly
    """
    print("Verifying test database setup...")
    
    conn = psycopg2.connect(**TEST_DB_CONFIG)
    cursor = conn.cursor()
    
    # Check that all required tables exist
    required_tables = [
        'emission_factors',
        'emission_records',
        'business_metrics',
        'audit_log',
        'emission_categories',
        'reporting_periods'
    ]
    
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_type = 'BASE TABLE'
    """)
    
    existing_tables = [row[0] for row in cursor.fetchall()]
    
    missing_tables = set(required_tables) - set(existing_tables)
    
    if missing_tables:
        print(f"ERROR: Missing tables: {missing_tables}")
        cursor.close()
        conn.close()
        return False
    
    print(f"✓ All required tables exist: {len(existing_tables)} tables found")
    
    # Check that views exist
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.views 
        WHERE table_schema = 'public'
    """)
    
    views = [row[0] for row in cursor.fetchall()]
    print(f"✓ Views created: {len(views)} views found")
    
    # Check that functions exist
    cursor.execute("""
        SELECT routine_name 
        FROM information_schema.routines 
        WHERE routine_schema = 'public' 
        AND routine_type = 'FUNCTION'
    """)
    
    functions = [row[0] for row in cursor.fetchall()]
    print(f"✓ Functions created: {len(functions)} functions found")
    
    cursor.close()
    conn.close()
    
    print("Test database verification completed successfully!")
    return True


def main():
    """
    Main setup function
    """
    print("=" * 70)
    print("Carbon Emissions Platform - Test Database Setup")
    print("=" * 70)
    
    try:
        # Step 1: Create test database
        create_test_database()
        
        # Step 2: Initialize schema
        initialize_test_schema()
        
        # Step 3: Verify setup
        if verify_test_database():
            print("\n" + "=" * 70)
            print("✓ Test database setup completed successfully!")
            print("=" * 70)
            print(f"\nTest database connection details:")
            print(f"  Host: {TEST_DB_CONFIG['host']}")
            print(f"  Port: {TEST_DB_CONFIG['port']}")
            print(f"  Database: {TEST_DB_CONFIG['database']}")
            print(f"  User: {TEST_DB_CONFIG['user']}")
            print("\nYou can now run integration tests with: pytest backend/tests/")
        else:
            print("\n" + "=" * 70)
            print("✗ Test database setup completed with warnings")
            print("=" * 70)
            sys.exit(1)
            
    except Exception as e:
        print("\n" + "=" * 70)
        print(f"✗ Error during test database setup: {e}")
        print("=" * 70)
        sys.exit(1)


if __name__ == "__main__":
    main()
