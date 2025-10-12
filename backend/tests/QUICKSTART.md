# Integration Testing Quick Start Guide

## Prerequisites

1. PostgreSQL server running on localhost:5432
2. Database user `ghg_user` with password `1234` (or set custom via environment variables)

## Setup (One-time)

### 1. Install dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Create and initialize test database

```bash
python tests/setup_test_db.py
```

Expected output:

```
======================================================================
Carbon Emissions Platform - Test Database Setup
======================================================================
Creating test database: ghg_platform_test
Test database 'ghg_platform_test' created successfully
Initializing test database schema...
Test database schema initialized successfully
Verifying test database setup...
✓ All required tables exist: 6 tables found
✓ Views created: 4 views found
✓ Functions created: 3 functions found

======================================================================
✓ Test database setup completed successfully!
======================================================================

Test database connection details:
  Host: localhost
  Port: 5432
  Database: ghg_platform_test
  User: ghg_user

You can now run integration tests with: pytest backend/tests/
```

## Running Tests

### Run all integration tests

```bash
pytest backend/tests/ -v
```

### Run specific test file

```bash
pytest backend/tests/test_integration_example.py -v
```

### Run specific test class

```bash
pytest backend/tests/test_integration_example.py::TestHistoricalAccuracy -v
```

### Run specific test

```bash
pytest backend/tests/test_integration_example.py::TestHistoricalAccuracy::test_get_valid_factor_for_2023 -v
```

### Run with output

```bash
pytest backend/tests/ -v -s
```

### Run with coverage

```bash
pytest backend/tests/ --cov=app --cov-report=html
```

## Custom Database Configuration

If your PostgreSQL setup is different, set these environment variables:

```bash
export TEST_DB_HOST=localhost
export TEST_DB_PORT=5432
export TEST_DB_NAME=ghg_platform_test
export TEST_DB_USER=ghg_user
export TEST_DB_PASSWORD=1234
```

Then run the setup script again:

```bash
python tests/setup_test_db.py
```

## Troubleshooting

### "Connection refused" error

- Ensure PostgreSQL is running: `pg_isready`
- Check connection settings match your PostgreSQL configuration

### "Database does not exist" error

- Run the setup script: `python tests/setup_test_db.py`

### "Permission denied" error

- Ensure the database user has CREATE DATABASE privileges
- Or create the database manually and run setup script again

### Tests fail with "relation does not exist"

- Re-run setup script to recreate schema: `python tests/setup_test_db.py`

### Import errors

- Ensure you're in the backend directory when running tests
- Install dependencies: `pip install -r requirements.txt`

## What Gets Tested

The integration tests verify:

1. **Database Setup**: Tables, views, and functions exist
2. **Fixtures**: Test data fixtures work correctly
3. **Historical Accuracy**: Emission factors are selected correctly based on date
4. **Boundary Conditions**: Factor selection on valid_from/valid_to dates
5. **Emission Calculations**: Records are created with correct calculations
6. **Data Integrity**: Different years use different factor versions
7. **Error Handling**: Invalid inputs raise appropriate errors

## Next Steps

After verifying the test infrastructure works:

1. Write integration tests for repositories (task 9.2)
2. Write end-to-end API tests (task 9.3)
3. Test historical accuracy with real scenarios
4. Test error conditions and edge cases

## Example Test Output

```
backend/tests/test_integration_example.py::TestDatabaseSetup::test_database_connection PASSED
backend/tests/test_integration_example.py::TestDatabaseSetup::test_tables_exist PASSED
backend/tests/test_integration_example.py::TestEmissionFactorFixtures::test_sample_emission_factors_structure PASSED
backend/tests/test_integration_example.py::TestEmissionFactorFixtures::test_seed_emission_factors PASSED
backend/tests/test_integration_example.py::TestHistoricalAccuracy::test_get_valid_factor_for_2023 PASSED
backend/tests/test_integration_example.py::TestHistoricalAccuracy::test_get_valid_factor_for_2024 PASSED
backend/tests/test_integration_example.py::TestHistoricalAccuracy::test_get_valid_factor_for_2022 PASSED
backend/tests/test_integration_example.py::TestHistoricalAccuracy::test_boundary_date_valid_from PASSED
backend/tests/test_integration_example.py::TestHistoricalAccuracy::test_boundary_date_valid_to PASSED
backend/tests/test_integration_example.py::TestEmissionRecordCreation::test_create_emission_record_2023 PASSED
backend/tests/test_integration_example.py::TestEmissionRecordCreation::test_create_emission_record_2024 PASSED
backend/tests/test_integration_example.py::TestEmissionRecordCreation::test_create_records_different_years_use_different_factors PASSED

========================= 12 passed in 2.34s =========================
```
