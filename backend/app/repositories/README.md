# Repository Layer - Usage Guide

## Overview

This directory contains the data access layer for the Carbon Emissions Platform. The repositories provide clean interfaces for database operations related to emissions and business metrics.

## Available Repositories

### EmissionRepository

Handles all emission-related database operations.

```python
from app.repositories import EmissionRepository

repo = EmissionRepository()
```

#### Methods

**1. Get Valid Emission Factor**

```python
# Get the emission factor that was valid on a specific date
factor = repo.get_valid_factor(
    activity_name="Diesel",
    scope=1,
    activity_date=date(2024, 1, 15)
)

# Returns:
# {
#     'factor_id': 3,
#     'co2e_per_unit': 2.73,
#     'activity_unit': 'litres',
#     'source': 'EPA 2024',
#     'valid_from': date(2024, 1, 1),
#     'valid_to': None
# }
```

**2. Get Emissions by Year and Scope**

```python
# Get emissions for multiple years, grouped by scope
emissions = repo.get_emissions_by_year_and_scope(
    years=[2023, 2024]
)

# Returns:
# [
#     {'year': 2024, 'scope': 1, 'total_emissions': 125000.5},
#     {'year': 2024, 'scope': 2, 'total_emissions': 85000.25},
#     {'year': 2023, 'scope': 1, 'total_emissions': 135000.75},
#     ...
# ]
```

**3. Get Total Emissions for Period**

```python
# Get total emissions for a date range
result = repo.get_total_emissions_for_period(
    start_date=date(2024, 1, 1),
    end_date=date(2024, 3, 31)
)

# Returns:
# {
#     'total_emissions': 125000.5,
#     'record_count': 450
# }
```

**4. Get Emissions by Source (Hotspots)**

```python
# Get top emission sources with optional filters
hotspots = repo.get_emissions_by_source(
    filters={
        'start_date': date(2024, 1, 1),
        'end_date': date(2024, 12, 31),
        'scope': 1,  # Optional: filter by scope
        'limit': 10  # Optional: default is 10
    }
)

# Returns:
# [
#     {
#         'activity_name': 'Diesel',
#         'scope': 1,
#         'total_emissions': 125000.5,
#         'record_count': 350,
#         'average_per_record': 357.14
#     },
#     ...
# ]
```

---

### BusinessMetricsRepository

Handles business metrics database operations.

```python
from app.repositories import BusinessMetricsRepository

repo = BusinessMetricsRepository()
```

#### Methods

**1. Get Metric Total for Period**

```python
# Get total value of a metric for a date range
result = repo.get_metric_total_for_period(
    metric_name="Tons of Steel Produced",
    start_date=date(2024, 1, 1),
    end_date=date(2024, 3, 31)
)

# Returns:
# {
#     'total_value': 150000.0,
#     'unit': 'tons',
#     'record_count': 3
# }

# Returns None if no data found
```

**2. Get Available Metrics**

```python
# Get list of all available metrics
metrics = repo.get_available_metrics()

# Returns:
# [
#     {
#         'metric_name': 'Number of Employees',
#         'metric_category': 'Operational',
#         'unit': 'employees'
#     },
#     {
#         'metric_name': 'Tons of Steel Produced',
#         'metric_category': 'Production',
#         'unit': 'tons'
#     }
# ]
```

---

## Error Handling

All repository methods include error handling and logging:

```python
try:
    factor = repo.get_valid_factor("Diesel", 1, date(2024, 1, 15))
    if factor is None:
        # No factor found for this date
        print("No emission factor available")
    else:
        # Use the factor
        print(f"Factor: {factor['co2e_per_unit']}")
except Exception as e:
    # Database error occurred
    print(f"Error: {e}")
```

---

## Best Practices

### 1. Always Check for None

Some methods return `None` when no data is found:

```python
factor = repo.get_valid_factor(...)
if factor is None:
    # Handle missing data
    raise ValueError("No emission factor found")
```

### 2. Use Context Managers

The repositories use context managers internally, so connections are automatically managed:

```python
# No need to manually manage connections
emissions = repo.get_emissions_by_year_and_scope([2023, 2024])
```

### 3. Validate Inputs

Always validate inputs before calling repository methods:

```python
if start_date > end_date:
    raise ValueError("start_date must be before end_date")

result = repo.get_total_emissions_for_period(start_date, end_date)
```

### 4. Handle Empty Results

Check for empty lists when expecting multiple results:

```python
hotspots = repo.get_emissions_by_source(filters)
if not hotspots:
    # No data found
    return {"message": "No emission data available"}
```

---

## Integration with Service Layer

Repositories are designed to be used by service classes:

```python
from app.repositories import EmissionRepository, BusinessMetricsRepository

class AnalyticsService:
    def __init__(self):
        self.emission_repo = EmissionRepository()
        self.metrics_repo = BusinessMetricsRepository()

    def calculate_intensity(self, start_date, end_date, metric_name):
        # Get emissions
        emissions_data = self.emission_repo.get_total_emissions_for_period(
            start_date, end_date
        )

        # Get production
        metrics_data = self.metrics_repo.get_metric_total_for_period(
            metric_name, start_date, end_date
        )

        # Calculate intensity
        if metrics_data and metrics_data['total_value'] > 0:
            intensity = emissions_data['total_emissions'] / metrics_data['total_value']
            return intensity
        else:
            raise ValueError("No production data available")
```

---

## Database Schema Dependencies

The repositories depend on these database tables:

- `emission_factors` - Versioned emission factors
- `emission_records` - Activity records with calculated emissions
- `business_metrics` - Production and operational metrics

Required indexes (already in schema):

- `idx_emission_factors_lookup`
- `idx_emission_records_date_scope`
- `idx_business_metrics_lookup`

---

## Logging

All repository methods log their operations:

```python
import logging

# Configure logging to see repository operations
logging.basicConfig(level=logging.DEBUG)

# Now repository calls will log:
# DEBUG: Found emission factor 3 for Diesel (scope 1) on 2024-01-15
# DEBUG: Retrieved 6 emission records for years [2023, 2024]
```

---

## Testing

For unit testing, you can mock the database cursor:

```python
from unittest.mock import patch, MagicMock

@patch('app.repositories.emission_repository.get_db_cursor')
def test_get_valid_factor(mock_cursor):
    # Setup mock
    mock_cursor.return_value.__enter__.return_value.fetchone.return_value = {
        'factor_id': 1,
        'co2e_per_unit': 2.73,
        'activity_unit': 'litres',
        'source': 'EPA 2024'
    }

    # Test
    repo = EmissionRepository()
    result = repo.get_valid_factor('Diesel', 1, date(2024, 1, 15))

    assert result['factor_id'] == 1
```

---

## Performance Considerations

1. **Use appropriate date ranges** - Avoid querying years of data unnecessarily
2. **Set reasonable limits** - Use the `limit` parameter in `get_emissions_by_source()`
3. **Cache results** - Consider caching frequently accessed data at the service layer
4. **Use indexes** - The database schema includes optimized indexes for all queries

---

## Support

For issues or questions about the repository layer:

1. Check the logs for detailed error messages
2. Verify database connection is working
3. Ensure required tables and indexes exist
4. Review the SQL queries in the implementation
