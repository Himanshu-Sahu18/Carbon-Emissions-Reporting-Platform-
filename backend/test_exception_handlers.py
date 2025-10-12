"""
Integration test for exception handlers with FastAPI
Tests that custom exceptions are properly caught and formatted by the API
"""
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from app.exceptions import (
    FactorNotFoundException,
    NoProductionDataException,
    InvalidDateRangeException,
    register_exception_handlers
)

# Create a test FastAPI app
app = FastAPI()

# Register exception handlers
register_exception_handlers(app)


# Test endpoints that raise custom exceptions
@app.get("/test/factor-not-found")
async def test_factor_not_found():
    raise FactorNotFoundException(
        activity_name="Test Activity",
        scope=1,
        activity_date="2024-01-01"
    )


@app.get("/test/no-production-data")
async def test_no_production_data():
    raise NoProductionDataException(
        metric_name="Test Metric",
        start_date="2024-01-01",
        end_date="2024-12-31"
    )


@app.get("/test/invalid-date-range")
async def test_invalid_date_range():
    raise InvalidDateRangeException(
        start_date="2024-12-31",
        end_date="2024-01-01",
        reason="End date must be after start date"
    )


@app.get("/test/unhandled-exception")
async def test_unhandled_exception():
    raise RuntimeError("This is an unhandled exception")


@app.get("/test/validation-error")
async def test_validation_error(value: int):
    return {"value": value}


def test_factor_not_found_handler():
    """Test that FactorNotFoundException is properly handled"""
    print("\nTesting FactorNotFoundException handler...")
    client = TestClient(app)
    response = client.get("/test/factor-not-found")
    
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "FACTOR_NOT_FOUND"
    assert "Test Activity" in data["error"]["message"]
    assert data["error"]["details"]["activity_name"] == "Test Activity"
    assert data["error"]["details"]["scope"] == 1
    
    print(f"✓ Status Code: {response.status_code}")
    print(f"✓ Response: {data}")


def test_no_production_data_handler():
    """Test that NoProductionDataException is properly handled"""
    print("\nTesting NoProductionDataException handler...")
    client = TestClient(app)
    response = client.get("/test/no-production-data")
    
    assert response.status_code == 422
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "NO_PRODUCTION_DATA"
    assert "Test Metric" in data["error"]["message"]
    assert data["error"]["details"]["metric_name"] == "Test Metric"
    
    print(f"✓ Status Code: {response.status_code}")
    print(f"✓ Response: {data}")


def test_invalid_date_range_handler():
    """Test that InvalidDateRangeException is properly handled"""
    print("\nTesting InvalidDateRangeException handler...")
    client = TestClient(app)
    response = client.get("/test/invalid-date-range")
    
    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "INVALID_DATE_RANGE"
    assert "End date must be after start date" in data["error"]["message"]
    
    print(f"✓ Status Code: {response.status_code}")
    print(f"✓ Response: {data}")


def test_unhandled_exception_handler():
    """Test that unhandled exceptions are caught and formatted"""
    print("\nTesting unhandled exception handler...")
    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/test/unhandled-exception")
    
    assert response.status_code == 500
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "INTERNAL_SERVER_ERROR"
    assert "unexpected error occurred" in data["error"]["message"].lower()
    
    print(f"✓ Status Code: {response.status_code}")
    print(f"✓ Response: {data}")


def test_validation_error_handler():
    """Test that validation errors are properly formatted"""
    print("\nTesting validation error handler...")
    client = TestClient(app)
    response = client.get("/test/validation-error?value=not_an_int")
    
    assert response.status_code == 422
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert "validation_errors" in data["error"]["details"]
    
    print(f"✓ Status Code: {response.status_code}")
    print(f"✓ Response: {data}")


def test_error_response_format():
    """Test that all error responses follow the standardized format"""
    print("\nTesting standardized error response format...")
    client = TestClient(app, raise_server_exceptions=False)
    
    endpoints = [
        "/test/factor-not-found",
        "/test/no-production-data",
        "/test/invalid-date-range",
        "/test/unhandled-exception"
    ]
    
    for endpoint in endpoints:
        response = client.get(endpoint)
        data = response.json()
        
        # Verify standardized format
        assert "error" in data, f"Missing 'error' key in {endpoint}"
        assert "code" in data["error"], f"Missing 'code' in {endpoint}"
        assert "message" in data["error"], f"Missing 'message' in {endpoint}"
        assert "details" in data["error"], f"Missing 'details' in {endpoint}"
        
        print(f"✓ {endpoint} follows standardized format")


if __name__ == "__main__":
    print("=" * 70)
    print("Exception Handler Integration Tests")
    print("=" * 70)
    
    test_factor_not_found_handler()
    test_no_production_data_handler()
    test_invalid_date_range_handler()
    test_unhandled_exception_handler()
    test_validation_error_handler()
    test_error_response_format()
    
    print("\n" + "=" * 70)
    print("All integration tests passed! ✓")
    print("=" * 70)
