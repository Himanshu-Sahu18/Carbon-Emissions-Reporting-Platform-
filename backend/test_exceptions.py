"""
Test script to verify custom exceptions and error handling
"""
from app.exceptions import (
    FactorNotFoundException,
    NoProductionDataException,
    InvalidDateRangeException,
    InvalidScopeException,
    DatabaseConnectionException,
    format_error_response
)


def test_factor_not_found_exception():
    """Test FactorNotFoundException"""
    print("Testing FactorNotFoundException...")
    try:
        raise FactorNotFoundException(
            activity_name="Diesel",
            scope=1,
            activity_date="2023-06-15"
        )
    except FactorNotFoundException as e:
        assert e.error_code == "FACTOR_NOT_FOUND"
        assert e.status_code == 404
        assert "Diesel" in e.message
        assert e.details["scope"] == 1
        print(f"✓ Error Code: {e.error_code}")
        print(f"✓ Status Code: {e.status_code}")
        print(f"✓ Message: {e.message}")
        print(f"✓ Details: {e.details}")


def test_no_production_data_exception():
    """Test NoProductionDataException"""
    print("\nTesting NoProductionDataException...")
    try:
        raise NoProductionDataException(
            metric_name="Tons of Steel Produced",
            start_date="2024-01-01",
            end_date="2024-03-31"
        )
    except NoProductionDataException as e:
        assert e.error_code == "NO_PRODUCTION_DATA"
        assert e.status_code == 422
        assert "Tons of Steel Produced" in e.message
        assert e.details["metric_name"] == "Tons of Steel Produced"
        print(f"✓ Error Code: {e.error_code}")
        print(f"✓ Status Code: {e.status_code}")
        print(f"✓ Message: {e.message}")
        print(f"✓ Details: {e.details}")


def test_invalid_date_range_exception():
    """Test InvalidDateRangeException"""
    print("\nTesting InvalidDateRangeException...")
    try:
        raise InvalidDateRangeException(
            start_date="2024-12-31",
            end_date="2024-01-01",
            reason="End date must be after start date"
        )
    except InvalidDateRangeException as e:
        assert e.error_code == "INVALID_DATE_RANGE"
        assert e.status_code == 400
        assert "End date must be after start date" in e.message
        assert e.details["start_date"] == "2024-12-31"
        print(f"✓ Error Code: {e.error_code}")
        print(f"✓ Status Code: {e.status_code}")
        print(f"✓ Message: {e.message}")
        print(f"✓ Details: {e.details}")


def test_invalid_scope_exception():
    """Test InvalidScopeException"""
    print("\nTesting InvalidScopeException...")
    try:
        raise InvalidScopeException(scope=5)
    except InvalidScopeException as e:
        assert e.error_code == "INVALID_SCOPE"
        assert e.status_code == 400
        assert "Invalid scope value" in e.message
        assert e.details["provided_scope"] == 5
        assert e.details["valid_scopes"] == [1, 2, 3]
        print(f"✓ Error Code: {e.error_code}")
        print(f"✓ Status Code: {e.status_code}")
        print(f"✓ Message: {e.message}")
        print(f"✓ Details: {e.details}")


def test_database_connection_exception():
    """Test DatabaseConnectionException"""
    print("\nTesting DatabaseConnectionException...")
    try:
        raise DatabaseConnectionException(
            message="Connection timeout",
            details={"host": "localhost", "port": 5432}
        )
    except DatabaseConnectionException as e:
        assert e.error_code == "DATABASE_ERROR"
        assert e.status_code == 503
        assert "Connection timeout" in e.message
        print(f"✓ Error Code: {e.error_code}")
        print(f"✓ Status Code: {e.status_code}")
        print(f"✓ Message: {e.message}")
        print(f"✓ Details: {e.details}")


def test_error_response_format():
    """Test standardized error response format"""
    print("\nTesting error response format...")
    response = format_error_response(
        error_code="TEST_ERROR",
        message="This is a test error",
        details={"field": "value"}
    )
    
    assert "error" in response
    assert response["error"]["code"] == "TEST_ERROR"
    assert response["error"]["message"] == "This is a test error"
    assert response["error"]["details"]["field"] == "value"
    print(f"✓ Response format: {response}")


if __name__ == "__main__":
    print("=" * 60)
    print("Custom Exceptions Test Suite")
    print("=" * 60)
    
    test_factor_not_found_exception()
    test_no_production_data_exception()
    test_invalid_date_range_exception()
    test_invalid_scope_exception()
    test_database_connection_exception()
    test_error_response_format()
    
    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)
