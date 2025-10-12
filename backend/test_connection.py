"""
Simple test script to verify database connection and pool functionality
"""
from app.database import get_db_cursor, db_pool

def test_database_connection():
    """Test basic database connectivity"""
    print("Testing database connection...")
    
    # Test health check
    is_healthy = db_pool.health_check()
    print(f"Database health check: {'✓ PASSED' if is_healthy else '✗ FAILED'}")
    
    # Test query execution
    try:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT version()")
            result = cursor.fetchone()
            print(f"PostgreSQL version: {result['version']}")
            print("Query execution: ✓ PASSED")
    except Exception as e:
        print(f"Query execution: ✗ FAILED - {e}")
        return False
    
    # Test emission_factors table
    try:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as count FROM emission_factors")
            result = cursor.fetchone()
            print(f"Emission factors count: {result['count']}")
            print("Table access: ✓ PASSED")
    except Exception as e:
        print(f"Table access: ✗ FAILED - {e}")
        return False
    
    print("\n✓ All database tests passed!")
    return True

if __name__ == "__main__":
    test_database_connection()
