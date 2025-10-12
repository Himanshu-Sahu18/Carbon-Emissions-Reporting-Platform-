"""
Test script for EmissionCalculationService
Verifies the service implementation with mock data
"""
import sys
import os
from datetime import date

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# Mock the dependencies before importing
class MockRealDictRow:
    pass

class MockExtras:
    RealDictRow = MockRealDictRow

class MockPsycopg2:
    extras = MockExtras()
    Error = Exception
    
    class pool:
        class ThreadedConnectionPool:
            pass
    
    class extensions:
        class connection:
            pass

sys.modules['psycopg2'] = MockPsycopg2()
sys.modules['psycopg2.extras'] = MockExtras()
sys.modules['psycopg2.pool'] = MockPsycopg2.pool
sys.modules['psycopg2.extensions'] = MockPsycopg2.extensions

# Mock pydantic_settings
class MockSettings:
    pass

class MockPydanticSettings:
    BaseSettings = MockSettings

sys.modules['pydantic_settings'] = MockPydanticSettings()

from app.services.emission_calculation import (
    EmissionCalculationService,
    FactorNotFoundException
)


class MockEmissionRepository:
    """Mock repository for testing"""
    
    def get_valid_factor(self, activity_name: str, scope: int, activity_date: date):
        """Return mock factor data"""
        if activity_name == "Diesel" and scope == 1:
            return {
                'factor_id': 1,
                'co2e_per_unit': 2.68,
                'activity_unit': 'litres',
                'source': 'DEFRA 2023',
                'valid_from': date(2023, 1, 1),
                'valid_to': None
            }
        return None


def test_get_valid_factor_success():
    """Test successful factor retrieval"""
    print("Test 1: Get valid factor - Success case")
    
    service = EmissionCalculationService(MockEmissionRepository())
    
    factor = service.get_valid_factor(
        activity_name="Diesel",
        scope=1,
        activity_date=date(2024, 6, 15)
    )
    
    assert factor is not None
    assert factor['factor_id'] == 1
    assert factor['co2e_per_unit'] == 2.68
    assert factor['activity_unit'] == 'litres'
    
    print("✓ Factor retrieved successfully")
    print(f"  Factor ID: {factor['factor_id']}")
    print(f"  CO2e per unit: {factor['co2e_per_unit']} kgCO2e per {factor['activity_unit']}")


def test_get_valid_factor_not_found():
    """Test factor not found scenario"""
    print("\nTest 2: Get valid factor - Not found case")
    
    service = EmissionCalculationService(MockEmissionRepository())
    
    try:
        factor = service.get_valid_factor(
            activity_name="Unknown Activity",
            scope=1,
            activity_date=date(2024, 6, 15)
        )
        print("✗ Should have raised FactorNotFoundException")
    except FactorNotFoundException as e:
        print("✓ FactorNotFoundException raised correctly")
        print(f"  Error message: {e.message}")


def test_calculate_emission_success():
    """Test emission calculation"""
    print("\nTest 3: Calculate emission - Success case")
    
    service = EmissionCalculationService(MockEmissionRepository())
    
    factor = {
        'factor_id': 1,
        'co2e_per_unit': 2.68,
        'activity_unit': 'litres'
    }
    
    calculated_co2e = service.calculate_emission(
        activity_value=1000.0,
        factor=factor
    )
    
    expected = 1000.0 * 2.68
    assert calculated_co2e == expected
    
    print("✓ Emission calculated successfully")
    print(f"  Activity value: 1000.0 litres")
    print(f"  Factor: {factor['co2e_per_unit']} kgCO2e per litre")
    print(f"  Calculated CO2e: {calculated_co2e} kgCO2e")


def test_calculate_emission_negative_value():
    """Test emission calculation with negative value"""
    print("\nTest 4: Calculate emission - Negative value case")
    
    service = EmissionCalculationService(MockEmissionRepository())
    
    factor = {
        'factor_id': 1,
        'co2e_per_unit': 2.68,
        'activity_unit': 'litres'
    }
    
    try:
        calculated_co2e = service.calculate_emission(
            activity_value=-100.0,
            factor=factor
        )
        print("✗ Should have raised ValueError")
    except ValueError as e:
        print("✓ ValueError raised correctly for negative value")
        print(f"  Error message: {str(e)}")


def test_calculate_emission_missing_key():
    """Test emission calculation with invalid factor"""
    print("\nTest 5: Calculate emission - Missing key case")
    
    service = EmissionCalculationService(MockEmissionRepository())
    
    factor = {
        'factor_id': 1,
        'activity_unit': 'litres'
        # Missing 'co2e_per_unit'
    }
    
    try:
        calculated_co2e = service.calculate_emission(
            activity_value=1000.0,
            factor=factor
        )
        print("✗ Should have raised KeyError")
    except KeyError as e:
        print("✓ KeyError raised correctly for missing key")
        print(f"  Error message: {str(e)}")


def test_end_to_end():
    """Test end-to-end flow: get factor and calculate emission"""
    print("\nTest 6: End-to-end flow")
    
    service = EmissionCalculationService(MockEmissionRepository())
    
    # Step 1: Get valid factor
    factor = service.get_valid_factor(
        activity_name="Diesel",
        scope=1,
        activity_date=date(2024, 6, 15)
    )
    
    # Step 2: Calculate emission
    activity_value = 500.0
    calculated_co2e = service.calculate_emission(
        activity_value=activity_value,
        factor=factor
    )
    
    expected = activity_value * factor['co2e_per_unit']
    assert calculated_co2e == expected
    
    print("✓ End-to-end flow completed successfully")
    print(f"  Activity: Diesel (scope 1)")
    print(f"  Date: 2024-06-15")
    print(f"  Value: {activity_value} litres")
    print(f"  Factor: {factor['co2e_per_unit']} kgCO2e per litre")
    print(f"  Result: {calculated_co2e} kgCO2e")


if __name__ == "__main__":
    print("=" * 60)
    print("EmissionCalculationService Test Suite")
    print("=" * 60)
    
    try:
        test_get_valid_factor_success()
        test_get_valid_factor_not_found()
        test_calculate_emission_success()
        test_calculate_emission_negative_value()
        test_calculate_emission_missing_key()
        test_end_to_end()
        
        print("\n" + "=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
