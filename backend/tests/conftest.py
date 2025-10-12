"""
Pytest configuration and fixtures for integration tests
Provides test database setup, fixtures, and helper functions
"""
import os
import pytest
import psycopg2
from psycopg2 import pool
from psycopg2.extensions import connection as Connection
from datetime import date, datetime, timedelta
from typing import Generator, Dict, List, Any
from contextlib import contextmanager

# Test database configuration
TEST_DB_CONFIG = {
    "host": os.getenv("TEST_DB_HOST", "localhost"),
    "port": int(os.getenv("TEST_DB_PORT", "5432")),
    "database": os.getenv("TEST_DB_NAME", "ghg_platform_test"),
    "user": os.getenv("TEST_DB_USER", "ghg_user"),
    "password": os.getenv("TEST_DB_PASSWORD", "1234"),
}


@pytest.fixture(scope="session")
def test_db_pool() -> Generator[pool.ThreadedConnectionPool, None, None]:
    """
    Create a connection pool for the test database (session-scoped)
    """
    db_pool = pool.ThreadedConnectionPool(
        minconn=1,
        maxconn=10,
        **TEST_DB_CONFIG
    )
    yield db_pool
    db_pool.closeall()


@contextmanager
def get_test_connection(db_pool: pool.ThreadedConnectionPool) -> Generator[Connection, None, None]:
    """
    Context manager for test database connections
    """
    conn = db_pool.getconn()
    try:
        yield conn
    finally:
        db_pool.putconn(conn)


@pytest.fixture(scope="function")
def db_connection(test_db_pool: pool.ThreadedConnectionPool) -> Generator[Connection, None, None]:
    """
    Provide a database connection for each test function
    Automatically rolls back changes after each test
    """
    with get_test_connection(test_db_pool) as conn:
        # Start a transaction
        conn.autocommit = False
        yield conn
        # Rollback after test
        conn.rollback()


@pytest.fixture(scope="function")
def clean_database(db_connection: Connection):
    """
    Clean all tables before each test
    """
    cursor = db_connection.cursor()
    
    # Disable triggers temporarily for faster cleanup
    cursor.execute("SET session_replication_role = 'replica';")
    
    # Delete data from all tables in reverse dependency order
    tables = [
        "audit_log",
        "emission_records",
        "business_metrics",
        "emission_factors",
        "emission_categories",
        "reporting_periods"
    ]
    
    for table in tables:
        cursor.execute(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;")
    
    # Re-enable triggers
    cursor.execute("SET session_replication_role = 'origin';")
    
    db_connection.commit()
    cursor.close()


# ============================================================================
# Test Data Fixtures - Emission Factors
# ============================================================================

@pytest.fixture
def sample_emission_factors() -> List[Dict[str, Any]]:
    """
    Sample emission factors with versioning for testing historical accuracy
    """
    return [
        # Diesel - Multiple versions showing factor changes over time
        {
            "activity_name": "Diesel",
            "scope": 1,
            "activity_unit": "litres",
            "co2e_per_unit": 2.68,
            "source": "EPA 2022",
            "valid_from": date(2022, 1, 1),
            "valid_to": date(2022, 12, 31),
            "created_by": "test_system"
        },
        {
            "activity_name": "Diesel",
            "scope": 1,
            "activity_unit": "litres",
            "co2e_per_unit": 2.71,
            "source": "EPA 2023",
            "valid_from": date(2023, 1, 1),
            "valid_to": date(2023, 12, 31),
            "created_by": "test_system"
        },
        {
            "activity_name": "Diesel",
            "scope": 1,
            "activity_unit": "litres",
            "co2e_per_unit": 2.73,
            "source": "EPA 2024",
            "valid_from": date(2024, 1, 1),
            "valid_to": None,  # Currently active
            "created_by": "test_system"
        },
        # Natural Gas - Two versions
        {
            "activity_name": "Natural Gas",
            "scope": 1,
            "activity_unit": "m3",
            "co2e_per_unit": 2.03,
            "source": "IPCC 2006",
            "valid_from": date(2022, 1, 1),
            "valid_to": date(2023, 12, 31),
            "created_by": "test_system"
        },
        {
            "activity_name": "Natural Gas",
            "scope": 1,
            "activity_unit": "m3",
            "co2e_per_unit": 2.05,
            "source": "IPCC 2024",
            "valid_from": date(2024, 1, 1),
            "valid_to": None,
            "created_by": "test_system"
        },
        # Grid Electricity - Scope 2, two versions
        {
            "activity_name": "Grid Electricity",
            "scope": 2,
            "activity_unit": "kWh",
            "co2e_per_unit": 0.45,
            "source": "CEA India 2023",
            "valid_from": date(2023, 1, 1),
            "valid_to": date(2023, 12, 31),
            "created_by": "test_system"
        },
        {
            "activity_name": "Grid Electricity",
            "scope": 2,
            "activity_unit": "kWh",
            "co2e_per_unit": 0.42,
            "source": "CEA India 2024",
            "valid_from": date(2024, 1, 1),
            "valid_to": None,
            "created_by": "test_system"
        },
        # Petrol - Single version
        {
            "activity_name": "Petrol",
            "scope": 1,
            "activity_unit": "litres",
            "co2e_per_unit": 2.31,
            "source": "EPA 2024",
            "valid_from": date(2024, 1, 1),
            "valid_to": None,
            "created_by": "test_system"
        },
        # Coal - Scope 1
        {
            "activity_name": "Coal",
            "scope": 1,
            "activity_unit": "tonnes",
            "co2e_per_unit": 2419.00,
            "source": "IPCC 2006",
            "valid_from": date(2022, 1, 1),
            "valid_to": None,
            "created_by": "test_system"
        },
        # Air Travel - Scope 3
        {
            "activity_name": "Air Travel",
            "scope": 3,
            "activity_unit": "km",
            "co2e_per_unit": 0.255,
            "source": "DEFRA 2024",
            "valid_from": date(2024, 1, 1),
            "valid_to": None,
            "created_by": "test_system"
        }
    ]


@pytest.fixture
def sample_business_metrics() -> List[Dict[str, Any]]:
    """
    Sample business metrics for intensity calculations
    """
    return [
        # Production metrics for 2023
        {
            "metric_name": "Tons of Steel Produced",
            "metric_category": "Production",
            "value": 45000.00,
            "unit": "tons",
            "metric_date": date(2023, 1, 31),
            "reporting_period": "Monthly",
            "created_by": "test_system"
        },
        {
            "metric_name": "Tons of Steel Produced",
            "metric_category": "Production",
            "value": 48000.00,
            "unit": "tons",
            "metric_date": date(2023, 2, 28),
            "reporting_period": "Monthly",
            "created_by": "test_system"
        },
        {
            "metric_name": "Tons of Steel Produced",
            "metric_category": "Production",
            "value": 47500.00,
            "unit": "tons",
            "metric_date": date(2023, 3, 31),
            "reporting_period": "Monthly",
            "created_by": "test_system"
        },
        # Production metrics for 2024
        {
            "metric_name": "Tons of Steel Produced",
            "metric_category": "Production",
            "value": 50000.00,
            "unit": "tons",
            "metric_date": date(2024, 1, 31),
            "reporting_period": "Monthly",
            "created_by": "test_system"
        },
        {
            "metric_name": "Tons of Steel Produced",
            "metric_category": "Production",
            "value": 52000.00,
            "unit": "tons",
            "metric_date": date(2024, 2, 29),
            "reporting_period": "Monthly",
            "created_by": "test_system"
        },
        {
            "metric_name": "Tons of Steel Produced",
            "metric_category": "Production",
            "value": 51000.00,
            "unit": "tons",
            "metric_date": date(2024, 3, 31),
            "reporting_period": "Monthly",
            "created_by": "test_system"
        },
        # Employee metrics
        {
            "metric_name": "Number of Employees",
            "metric_category": "Operational",
            "value": 1200.00,
            "unit": "employees",
            "metric_date": date(2023, 12, 31),
            "reporting_period": "Annual",
            "created_by": "test_system"
        },
        {
            "metric_name": "Number of Employees",
            "metric_category": "Operational",
            "value": 1250.00,
            "unit": "employees",
            "metric_date": date(2024, 12, 31),
            "reporting_period": "Annual",
            "created_by": "test_system"
        },
        # Revenue metrics
        {
            "metric_name": "Revenue",
            "metric_category": "Financial",
            "value": 5000000.00,
            "unit": "USD",
            "metric_date": date(2023, 12, 31),
            "reporting_period": "Annual",
            "created_by": "test_system"
        },
        {
            "metric_name": "Revenue",
            "metric_category": "Financial",
            "value": 5500000.00,
            "unit": "USD",
            "metric_date": date(2024, 12, 31),
            "reporting_period": "Annual",
            "created_by": "test_system"
        }
    ]


# ============================================================================
# Helper Functions for Seeding Test Data
# ============================================================================

def seed_emission_factors(conn: Connection, factors: List[Dict[str, Any]]) -> List[int]:
    """
    Insert emission factors into the test database
    
    Args:
        conn: Database connection
        factors: List of emission factor dictionaries
    
    Returns:
        List of inserted factor_ids
    """
    cursor = conn.cursor()
    factor_ids = []
    
    insert_query = """
        INSERT INTO emission_factors (
            activity_name, scope, activity_unit, co2e_per_unit, 
            source, valid_from, valid_to, created_by
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING factor_id
    """
    
    for factor in factors:
        cursor.execute(insert_query, (
            factor["activity_name"],
            factor["scope"],
            factor["activity_unit"],
            factor["co2e_per_unit"],
            factor["source"],
            factor["valid_from"],
            factor["valid_to"],
            factor["created_by"]
        ))
        factor_id = cursor.fetchone()[0]
        factor_ids.append(factor_id)
    
    conn.commit()
    cursor.close()
    return factor_ids


def seed_business_metrics(conn: Connection, metrics: List[Dict[str, Any]]) -> List[int]:
    """
    Insert business metrics into the test database
    
    Args:
        conn: Database connection
        metrics: List of business metric dictionaries
    
    Returns:
        List of inserted metric_ids
    """
    cursor = conn.cursor()
    metric_ids = []
    
    insert_query = """
        INSERT INTO business_metrics (
            metric_name, metric_category, value, unit, 
            metric_date, reporting_period, created_by
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING metric_id
    """
    
    for metric in metrics:
        cursor.execute(insert_query, (
            metric["metric_name"],
            metric["metric_category"],
            metric["value"],
            metric["unit"],
            metric["metric_date"],
            metric["reporting_period"],
            metric["created_by"]
        ))
        metric_id = cursor.fetchone()[0]
        metric_ids.append(metric_id)
    
    conn.commit()
    cursor.close()
    return metric_ids


def seed_emission_records(
    conn: Connection, 
    records: List[Dict[str, Any]]
) -> List[int]:
    """
    Insert emission records into the test database
    
    Args:
        conn: Database connection
        records: List of emission record dictionaries
            Each record should contain:
            - activity_date, activity_name, scope, activity_value, 
            - activity_unit, factor_id, calculated_co2e, created_by
    
    Returns:
        List of inserted record_ids
    """
    cursor = conn.cursor()
    record_ids = []
    
    insert_query = """
        INSERT INTO emission_records (
            activity_date, activity_name, scope, activity_value,
            activity_unit, factor_id, calculated_co2e, created_by,
            location, department
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING record_id
    """
    
    for record in records:
        cursor.execute(insert_query, (
            record["activity_date"],
            record["activity_name"],
            record["scope"],
            record["activity_value"],
            record["activity_unit"],
            record["factor_id"],
            record["calculated_co2e"],
            record.get("created_by", "test_system"),
            record.get("location"),
            record.get("department")
        ))
        record_id = cursor.fetchone()[0]
        record_ids.append(record_id)
    
    conn.commit()
    cursor.close()
    return record_ids


def get_valid_factor_id(
    conn: Connection,
    activity_name: str,
    scope: int,
    activity_date: date
) -> int:
    """
    Get the valid factor_id for a given activity and date
    Mimics the historical accuracy logic
    
    Args:
        conn: Database connection
        activity_name: Name of the activity
        scope: GHG scope (1, 2, or 3)
        activity_date: Date of the activity
    
    Returns:
        factor_id of the valid emission factor
    
    Raises:
        ValueError: If no valid factor is found
    """
    cursor = conn.cursor()
    
    query = """
        SELECT factor_id, co2e_per_unit, activity_unit
        FROM emission_factors
        WHERE activity_name = %s
          AND scope = %s
          AND valid_from <= %s
          AND (valid_to >= %s OR valid_to IS NULL)
        ORDER BY valid_from DESC, created_at DESC
        LIMIT 1
    """
    
    cursor.execute(query, (activity_name, scope, activity_date, activity_date))
    result = cursor.fetchone()
    cursor.close()
    
    if result is None:
        raise ValueError(
            f"No valid emission factor found for {activity_name} "
            f"(scope {scope}) on {activity_date}"
        )
    
    return result[0]


def create_emission_record_with_factor(
    conn: Connection,
    activity_date: date,
    activity_name: str,
    scope: int,
    activity_value: float,
    activity_unit: str,
    location: str = None,
    department: str = None
) -> int:
    """
    Create an emission record with automatic factor lookup
    This simulates the real emission calculation flow
    
    Args:
        conn: Database connection
        activity_date: Date of the activity
        activity_name: Name of the activity
        scope: GHG scope
        activity_value: Amount of activity
        activity_unit: Unit of measurement
        location: Optional location
        department: Optional department
    
    Returns:
        record_id of the created emission record
    """
    cursor = conn.cursor()
    
    # Get the valid factor for this date
    factor_query = """
        SELECT factor_id, co2e_per_unit, activity_unit
        FROM emission_factors
        WHERE activity_name = %s
          AND scope = %s
          AND valid_from <= %s
          AND (valid_to >= %s OR valid_to IS NULL)
        ORDER BY valid_from DESC, created_at DESC
        LIMIT 1
    """
    
    cursor.execute(factor_query, (activity_name, scope, activity_date, activity_date))
    factor_result = cursor.fetchone()
    
    if factor_result is None:
        cursor.close()
        raise ValueError(
            f"No valid emission factor found for {activity_name} "
            f"(scope {scope}) on {activity_date}"
        )
    
    factor_id, co2e_per_unit, factor_unit = factor_result
    
    # Verify units match
    if activity_unit != factor_unit:
        cursor.close()
        raise ValueError(
            f"Unit mismatch: activity uses '{activity_unit}' "
            f"but factor uses '{factor_unit}'"
        )
    
    # Calculate emissions
    calculated_co2e = activity_value * co2e_per_unit
    
    # Insert the emission record
    insert_query = """
        INSERT INTO emission_records (
            activity_date, activity_name, scope, activity_value,
            activity_unit, factor_id, calculated_co2e, created_by,
            location, department
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING record_id
    """
    
    cursor.execute(insert_query, (
        activity_date,
        activity_name,
        scope,
        activity_value,
        activity_unit,
        factor_id,
        calculated_co2e,
        "test_system",
        location,
        department
    ))
    
    record_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    
    return record_id


# ============================================================================
# Composite Fixtures - Pre-seeded Database States
# ============================================================================

@pytest.fixture
def db_with_factors(db_connection: Connection, clean_database, sample_emission_factors):
    """
    Database with emission factors seeded
    """
    seed_emission_factors(db_connection, sample_emission_factors)
    return db_connection


@pytest.fixture
def db_with_metrics(db_connection: Connection, clean_database, sample_business_metrics):
    """
    Database with business metrics seeded
    """
    seed_business_metrics(db_connection, sample_business_metrics)
    return db_connection


@pytest.fixture
def db_with_factors_and_metrics(
    db_connection: Connection, 
    clean_database, 
    sample_emission_factors,
    sample_business_metrics
):
    """
    Database with both emission factors and business metrics seeded
    """
    seed_emission_factors(db_connection, sample_emission_factors)
    seed_business_metrics(db_connection, sample_business_metrics)
    return db_connection


@pytest.fixture
def db_with_full_test_data(db_with_factors_and_metrics: Connection):
    """
    Database with factors, metrics, and sample emission records
    Creates a realistic dataset spanning 2023-2024 with historical factor changes
    """
    conn = db_with_factors_and_metrics
    
    # Create emission records for 2023 using 2023 factors
    records_2023 = [
        # Diesel usage in 2023 (should use factor with co2e_per_unit=2.71)
        {
            "activity_date": date(2023, 1, 15),
            "activity_name": "Diesel",
            "scope": 1,
            "activity_value": 1000.0,
            "activity_unit": "litres",
            "location": "Plant A",
            "department": "Operations"
        },
        {
            "activity_date": date(2023, 6, 15),
            "activity_name": "Diesel",
            "scope": 1,
            "activity_value": 1500.0,
            "activity_unit": "litres",
            "location": "Plant A",
            "department": "Operations"
        },
        # Grid Electricity in 2023 (should use factor with co2e_per_unit=0.45)
        {
            "activity_date": date(2023, 1, 31),
            "activity_name": "Grid Electricity",
            "scope": 2,
            "activity_value": 50000.0,
            "activity_unit": "kWh",
            "location": "Plant A",
            "department": "Operations"
        },
        {
            "activity_date": date(2023, 2, 28),
            "activity_name": "Grid Electricity",
            "scope": 2,
            "activity_value": 52000.0,
            "activity_unit": "kWh",
            "location": "Plant A",
            "department": "Operations"
        },
        # Natural Gas in 2023
        {
            "activity_date": date(2023, 3, 15),
            "activity_name": "Natural Gas",
            "scope": 1,
            "activity_value": 2000.0,
            "activity_unit": "m3",
            "location": "Plant B",
            "department": "Production"
        }
    ]
    
    # Create emission records for 2024 using 2024 factors
    records_2024 = [
        # Diesel usage in 2024 (should use factor with co2e_per_unit=2.73)
        {
            "activity_date": date(2024, 1, 15),
            "activity_name": "Diesel",
            "scope": 1,
            "activity_value": 1000.0,
            "activity_unit": "litres",
            "location": "Plant A",
            "department": "Operations"
        },
        {
            "activity_date": date(2024, 6, 15),
            "activity_name": "Diesel",
            "scope": 1,
            "activity_value": 1200.0,
            "activity_unit": "litres",
            "location": "Plant A",
            "department": "Operations"
        },
        # Grid Electricity in 2024 (should use factor with co2e_per_unit=0.42)
        {
            "activity_date": date(2024, 1, 31),
            "activity_name": "Grid Electricity",
            "scope": 2,
            "activity_value": 55000.0,
            "activity_unit": "kWh",
            "location": "Plant A",
            "department": "Operations"
        },
        {
            "activity_date": date(2024, 2, 29),
            "activity_name": "Grid Electricity",
            "scope": 2,
            "activity_value": 58000.0,
            "activity_unit": "kWh",
            "location": "Plant A",
            "department": "Operations"
        },
        # Natural Gas in 2024
        {
            "activity_date": date(2024, 3, 15),
            "activity_name": "Natural Gas",
            "scope": 1,
            "activity_value": 2500.0,
            "activity_unit": "m3",
            "location": "Plant B",
            "department": "Production"
        },
        # Air Travel in 2024 (Scope 3)
        {
            "activity_date": date(2024, 4, 10),
            "activity_name": "Air Travel",
            "scope": 3,
            "activity_value": 5000.0,
            "activity_unit": "km",
            "location": "Corporate",
            "department": "Sales"
        }
    ]
    
    # Insert all records using the helper function
    for record in records_2023 + records_2024:
        create_emission_record_with_factor(conn, **record)
    
    return conn
