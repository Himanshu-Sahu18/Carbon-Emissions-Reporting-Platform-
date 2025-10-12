# Carbon Emissions Platform - Backend

## Overview

The Carbon Emissions Platform is a comprehensive API for tracking, analyzing, and reporting carbon emissions with **historical accuracy** at its core. Built with FastAPI and PostgreSQL, it provides advanced analytics capabilities for sustainability teams to measure, monitor, and reduce their carbon footprint.

### Key Features

- **📊 Year-over-Year Emissions Comparison** - Track progress toward reduction goals
- **⚡ Emission Intensity Calculation** - Measure carbon efficiency per unit of production
- **🎯 Emission Hotspot Analysis** - Identify highest-contributing emission sources
- **🔒 Historical Accuracy** - Immutable historical data using versioned emission factors
- **🚀 High Performance** - Optimized SQL queries with connection pooling
- **📝 Comprehensive Documentation** - OpenAPI/Swagger with interactive docs

### Quick Links

- **Interactive API Docs:** http://localhost:8000/docs
- **API Documentation:** [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)
- **Health Check:** http://localhost:8000/health

---

## Table of Contents

1. [Project Structure](#project-structure)
2. [Historical Accuracy Mechanism](#historical-accuracy-mechanism)
3. [Getting Started](#getting-started)
4. [API Endpoints](#api-endpoints)
5. [Configuration](#configuration)
6. [Database Connection](#database-connection)
7. [Development](#development)
8. [Testing](#testing)
9. [Deployment](#deployment)

---

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── config.py              # Configuration management
│   ├── database.py            # Database connection pooling
│   ├── models/                # Pydantic models (request/response)
│   ├── services/              # Business logic layer
│   ├── repositories/          # Data access layer
│   └── routers/               # API route handlers
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Container configuration
└── test_connection.py         # Database connection test script
```

## Configuration

The application uses environment variables for configuration. These are defined in `app/config.py` and loaded from the environment:

### Database Configuration

- `DB_HOST`: Database host (default: localhost)
- `DB_PORT`: Database port (default: 5432)
- `DB_NAME`: Database name (default: ghg_platform)
- `DB_USER`: Database user (default: ghg_user)
- `DB_PASSWORD`: Database password (default: 1234)

### Connection Pool Settings

- `DB_POOL_SIZE`: Maximum number of connections (default: 20)
- `DB_MAX_OVERFLOW`: Additional connections beyond pool size (default: 10)
- `DB_POOL_TIMEOUT`: Connection timeout in seconds (default: 30)
- `DB_POOL_RECYCLE`: Connection recycle time in seconds (default: 3600)

### Application Settings

- `API_KEY`: Optional API key for authentication
- `LOG_LEVEL`: Logging level (default: INFO)

## Database Connection

The `app/database.py` module implements a thread-safe connection pool using psycopg2:

### Features

- **Connection Pooling**: Efficient connection reuse with configurable pool size
- **Context Managers**: Automatic connection and cursor management
- **Error Handling**: Automatic rollback on errors
- **Health Checks**: Built-in database connectivity verification
- **Dictionary Cursors**: Results returned as dictionaries for easy access

### Usage Examples

#### Using Connection Context Manager

```python
from app.database import get_db_connection

with get_db_connection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM emission_factors")
    results = cursor.fetchall()
```

#### Using Cursor Context Manager

```python
from app.database import get_db_cursor

# Read-only query
with get_db_cursor() as cursor:
    cursor.execute("SELECT * FROM emission_factors WHERE scope = %s", (1,))
    results = cursor.fetchall()

# Write query with commit
with get_db_cursor(commit=True) as cursor:
    cursor.execute(
        "INSERT INTO emission_records (activity_date, activity_name, ...) VALUES (%s, %s, ...)",
        (date, name, ...)
    )
```

#### Using Helper Functions

```python
from app.database import execute_query, execute_transaction

# Simple query
results = execute_query("SELECT * FROM emission_factors WHERE scope = %s", (1,))

# Transaction with multiple queries
queries = [
    ("INSERT INTO table1 VALUES (%s)", (value1,)),
    ("UPDATE table2 SET col = %s WHERE id = %s", (value2, id))
]
execute_transaction(queries)
```

---

## Historical Accuracy Mechanism

### The Foundation of Trust

All emission calculations use the emission factors that were **valid on the activity date**, ensuring:

- ✅ **Immutable Historical Data** - Past calculations never change when factors are updated
- ✅ **Complete Audit Trail** - Track which factor version was used for each calculation
- ✅ **Accurate Comparisons** - Year-over-year analysis uses historically correct factors

### How It Works

#### 1. Versioned Emission Factors

```sql
CREATE TABLE emission_factors (
    factor_id SERIAL PRIMARY KEY,
    activity_name VARCHAR(255) NOT NULL,
    scope INTEGER NOT NULL,
    co2e_per_unit DECIMAL(10, 6) NOT NULL,
    valid_from DATE NOT NULL,        -- Factor becomes valid
    valid_to DATE,                    -- NULL = currently active
    ...
);
```

#### 2. Temporal Factor Lookup

When creating an emission record for activity on `2023-06-15`:

```sql
SELECT factor_id, co2e_per_unit
FROM emission_factors
WHERE activity_name = 'Diesel'
  AND scope = 1
  AND valid_from <= '2023-06-15'
  AND (valid_to >= '2023-06-15' OR valid_to IS NULL)
ORDER BY valid_from DESC
LIMIT 1;
```

#### 3. Permanent Factor Linkage

```sql
INSERT INTO emission_records (
    factor_id,              -- Permanent link to factor version
    activity_date,
    calculated_co2e,
    ...
) VALUES (2, '2023-06-15', 2710.0, ...);
```

#### Example Timeline

```
2023-01-01: Factor v1 created (co2e: 2.68 kgCO₂e/litre)
2023-06-15: Activity recorded → Uses Factor v1 ✓
2024-01-01: Factor v2 created (co2e: 2.73 kgCO₂e/litre)
            Factor v1 updated (valid_to: 2023-12-31)
2024-06-15: Activity recorded → Uses Factor v2 ✓

Result: Historical accuracy preserved!
```

For detailed explanation, see [API_DOCUMENTATION.md](./API_DOCUMENTATION.md#historical-accuracy-mechanism).

---

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- PostgreSQL 15+ (if running without Docker)

### Quick Start with Docker

1. **Clone the repository**

```bash
git clone <repository-url>
cd carbon-emissions-platform
```

2. **Start the services**

```bash
docker-compose up -d
```

3. **Verify the application is running**

```bash
curl http://localhost:8000/health
```

4. **Access the interactive documentation**

Open your browser to: http://localhost:8000/docs

### Local Development Setup

1. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**

```bash
cd backend
pip install -r requirements.txt
```

3. **Set environment variables**

```bash
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=ghg_platform
export DB_USER=ghg_user
export DB_PASSWORD=1234
```

4. **Run the application**

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## API Endpoints

### Analytics Endpoints

#### 1. Year-over-Year (YoY) Emissions Comparison

```http
GET /api/analytics/yoy?current_year=2024&previous_year=2023
```

**Purpose:** Compare total emissions by scope between two years to track reduction progress.

**Example Response:**

```json
{
  "current_year": 2024,
  "previous_year": 2023,
  "current_year_data": [
    {"scope": 1, "total_emissions": 125000.5, "unit": "kgCO2e"},
    {"scope": 2, "total_emissions": 85000.25, "unit": "kgCO2e"},
    {"scope": 3, "total_emissions": 45000.0, "unit": "kgCO2e"}
  ],
  "previous_year_data": [...],
  "comparison": {
    "total_current": 255000.75,
    "total_previous": 275001.25,
    "change_percentage": -7.27,
    "change_absolute": -20000.5
  }
}
```

**Use Cases:**

- Track progress toward emission reduction goals
- Report annual sustainability metrics
- Identify which scopes improved or worsened

---

#### 2. Emission Intensity Calculation

```http
GET /api/analytics/intensity?start_date=2024-01-01&end_date=2024-03-31&metric_name=Tons%20of%20Steel%20Produced
```

**Purpose:** Calculate carbon efficiency as kgCO₂e per unit of production.

**Example Response:**

```json
{
  "period": {
    "start_date": "2024-01-01",
    "end_date": "2024-03-31"
  },
  "metric_name": "Tons of Steel Produced",
  "total_emissions": 125000.5,
  "total_production": 150000.0,
  "production_unit": "tons",
  "intensity": 0.8333,
  "intensity_unit": "kgCO2e per tons",
  "record_count": 450
}
```

**Use Cases:**

- Measure operational efficiency improvements
- Normalize emissions against production volume
- Compare efficiency across facilities or time periods
- Benchmark against industry standards

---

#### 3. Emission Hotspot Analysis

```http
GET /api/analytics/hotspots?start_date=2024-01-01&end_date=2024-12-31&limit=5
```

**Purpose:** Identify which emission sources contribute the most to total footprint.

**Example Response:**

```json
{
  "period": {
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "limit": 5
  },
  "total_emissions": 255000.75,
  "hotspots": [
    {
      "activity_name": "Diesel",
      "scope": 1,
      "total_emissions": 125000.5,
      "percentage": 49.02,
      "record_count": 350,
      "average_per_record": 357.14
    },
    {
      "activity_name": "Grid Electricity",
      "scope": 2,
      "total_emissions": 85000.25,
      "percentage": 33.33,
      "record_count": 200,
      "average_per_record": 425.0
    }
  ]
}
```

**Use Cases:**

- Prioritize reduction efforts on highest-impact sources
- Identify inefficient activities (high average per record)
- Analyze emissions by scope or time period
- Support strategic decision-making

---

### System Endpoints

#### Health Check

```http
GET /health
```

Returns application and database health status.

**Response:**

```json
{
  "status": "healthy",
  "application": "Carbon Emissions Platform",
  "version": "1.0.0",
  "database": {
    "connected": true,
    "host": "db",
    "database": "ghg_platform"
  }
}
```

#### Root

```http
GET /
```

Returns welcome message and API navigation links.

---

### Complete API Documentation

For comprehensive API documentation including:

- Detailed endpoint specifications
- Request/response schemas
- Error handling
- Authentication
- Code examples

See: **[API_DOCUMENTATION.md](./API_DOCUMENTATION.md)**

---

## Running the Application

### Using Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

### Testing Database Connection

```bash
# Run connection test
docker exec ghg_backend python test_connection.py
```

### Accessing the API

- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## Development

### Adding New Dependencies

1. Add package to `requirements.txt`
2. Rebuild container: `docker-compose up -d --build backend`

### Database Migrations

The database schema is initialized from `init.sql` on first startup. The schema includes:

- Versioned emission factors
- Emission records with historical accuracy
- Business metrics for intensity calculations
- Comprehensive audit logging

---

## Testing

### Running Tests

```bash
# Run all tests
docker exec ghg_backend pytest

# Run with coverage
docker exec ghg_backend pytest --cov=app --cov-report=html

# Run specific test file
docker exec ghg_backend pytest tests/test_analytics_service.py

# Run with verbose output
docker exec ghg_backend pytest -v
```

### Test Database Connection

```bash
docker exec ghg_backend python test_connection.py
```

### Integration Tests

Integration tests are available in the `tests/` directory:

```bash
# Run integration tests
docker exec ghg_backend pytest tests/test_integration_example.py -v
```

For detailed testing documentation, see [tests/README.md](./tests/README.md).

---

## Deployment

### Docker Deployment

The application is containerized and ready for deployment:

```bash
# Build production image
docker build -t ghg-backend:latest .

# Run container
docker run -d \
  -p 8000:8000 \
  -e DB_HOST=your-db-host \
  -e DB_PASSWORD=your-secure-password \
  --name ghg-backend \
  ghg-backend:latest
```

### Environment Variables for Production

```bash
# Database
DB_HOST=production-db-host
DB_PORT=5432
DB_NAME=ghg_platform
DB_USER=ghg_user
DB_PASSWORD=<secure-password>

# Connection Pool
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=10
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=3600

# Application
LOG_LEVEL=INFO
API_KEY=<secure-api-key>
```

### Health Checks

Configure health checks for container orchestration:

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

### Performance Tuning

**Database Connection Pool:**

- Adjust `DB_POOL_SIZE` based on expected concurrent requests
- Monitor connection usage and adjust `DB_MAX_OVERFLOW`
- Set `DB_POOL_RECYCLE` to prevent stale connections

**Application Workers:**

```bash
# Run with multiple workers (Gunicorn)
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

---

## Architecture

### Layered Architecture

```
┌─────────────────────────────────────────┐
│         API Layer (FastAPI)             │
│  - Request validation (Pydantic)        │
│  - Response formatting                  │
│  - Error handling                       │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│       Service Layer (Business Logic)    │
│  - AnalyticsService                     │
│  - EmissionCalculationService           │
│  - Business rules & calculations        │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│     Repository Layer (Data Access)      │
│  - EmissionRepository                   │
│  - BusinessMetricsRepository            │
│  - SQL query construction               │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│      Database Layer (PostgreSQL)        │
│  - Versioned emission factors           │
│  - Emission records                     │
│  - Business metrics                     │
└─────────────────────────────────────────┘
```

### Design Principles

- **Separation of Concerns** - Clear boundaries between layers
- **Dependency Injection** - Services injected via FastAPI dependencies
- **Historical Accuracy** - Immutable factor linkage in data model
- **Performance** - Connection pooling and optimized queries
- **Testability** - Each layer independently testable

---

## Requirements Addressed

This implementation addresses all requirements from the specification:

### Requirement 1: Historical Accuracy Foundation

- **1.1**: Emission factors stored with `valid_from` and `valid_to` columns ✅
- **1.2**: Active factors have `NULL` in `valid_to` column ✅
- **1.3**: Historical factor lookup using date-aware queries ✅
- **1.4**: Permanent `factor_id` linkage in emission records ✅
- **1.5**: Date-specific factor selection for calculations ✅
- **1.6**: Multiple factor versions supported with temporal queries ✅

### Requirement 2: Year-over-Year Emissions API

- **2.1-2.7**: Full YoY comparison with scope grouping and change calculations ✅

### Requirement 3: Emission Intensity API

- **3.1-3.7**: Intensity calculation with production metrics and zero-check protection ✅

### Requirement 4: Emission Hotspot API

- **4.1-4.8**: Hotspot analysis with filtering, sorting, and percentage calculations ✅

---

## API Documentation

### Interactive Documentation

- **Swagger UI:** http://localhost:8000/docs

  - Try out endpoints directly in browser
  - View request/response schemas
  - See example responses

- **ReDoc:** http://localhost:8000/redoc
  - Clean, readable documentation
  - Searchable endpoint list
  - Detailed schema documentation

### OpenAPI Specification

Download the OpenAPI 3.0 spec:

```bash
curl http://localhost:8000/openapi.json > openapi.json
```

Use for:

- Generating client libraries
- Importing into API testing tools (Postman, Insomnia)
- Integrating with API gateways

---

## Code Documentation

### Service Layer Docstrings

All service methods include comprehensive docstrings:

```python
def get_yoy_emissions(self, current_year: int, previous_year: int) -> Dict[str, Any]:
    """
    Retrieve and compare emissions between two years, grouped by scope.
    Implements Year-over-Year analysis with comparison calculations.

    Args:
        current_year: The current year to analyze
        previous_year: The previous year for comparison

    Returns:
        Dictionary containing YoY comparison data with scope breakdowns

    Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7
    """
```

### Repository Layer Docstrings

All repository methods document their SQL queries and return types:

```python
def get_valid_factor(self, activity_name: str, scope: int, activity_date: date) -> Optional[Dict[str, Any]]:
    """
    Retrieve the emission factor that was valid on a specific date.
    Implements time-aware query to ensure historical accuracy.

    Args:
        activity_name: Name of the activity (e.g., 'Diesel')
        scope: GHG Protocol scope (1, 2, or 3)
        activity_date: The date the activity occurred

    Returns:
        Dictionary containing factor details or None if not found

    Requirements: 1.3, 1.4, 1.5, 1.6
    """
```

---

## Support & Contributing

### Getting Help

- **Documentation:** [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)
- **Interactive Docs:** http://localhost:8000/docs
- **Health Status:** http://localhost:8000/health

### Reporting Issues

When reporting issues, please include:

- API endpoint and request parameters
- Expected vs. actual behavior
- Error messages and status codes
- Application logs (if available)

### Development Guidelines

1. **Code Style:** Follow PEP 8 guidelines
2. **Documentation:** Add docstrings to all public methods
3. **Testing:** Write tests for new features
4. **Logging:** Use appropriate log levels (DEBUG, INFO, WARNING, ERROR)
5. **Error Handling:** Use custom exceptions with meaningful messages

---

## License

MIT License - See LICENSE file for details

---

## Changelog

### Version 1.0.0 (Current)

**Features:**

- ✅ Year-over-Year emissions comparison API
- ✅ Emission intensity calculation API
- ✅ Emission hotspot analysis API
- ✅ Historical accuracy foundation with versioned factors
- ✅ Comprehensive error handling with custom exceptions
- ✅ OpenAPI/Swagger documentation
- ✅ Connection pooling for high performance
- ✅ Health check endpoint
- ✅ Docker containerization

**Documentation:**

- ✅ Comprehensive API documentation
- ✅ Code docstrings for all services and repositories
- ✅ README with usage examples
- ✅ Historical accuracy mechanism documentation
- ✅ Interactive Swagger UI

---

**Built with ❤️ for a sustainable future**
