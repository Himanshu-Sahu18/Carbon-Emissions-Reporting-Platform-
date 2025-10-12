"""
Carbon Emissions Platform - Main Application Entry Point
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_database, close_database, db_pool
from app.exceptions import register_exception_handlers
from app.routers import analytics, emissions, metrics

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI application with comprehensive OpenAPI documentation
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
# Carbon Emissions Platform - Advanced Analytics & Reporting Engine

A comprehensive API for tracking, analyzing, and reporting carbon emissions with **historical accuracy** at its core.

## Key Features

### 🎯 Historical Accuracy Foundation
All emission calculations use the emission factors that were valid on the activity date, ensuring:
- **Immutable historical data** - Past calculations never change when factors are updated
- **Audit trail** - Complete traceability of which factor version was used
- **Temporal queries** - Factor selection based on validity periods (valid_from/valid_to)

### 📊 Analytics Capabilities

1. **Year-over-Year (YoY) Emissions Comparison**
   - Compare emissions between years by scope (1, 2, 3)
   - Track progress toward reduction goals
   - Calculate percentage and absolute changes

2. **Emission Intensity Calculation**
   - Calculate carbon efficiency (kgCO₂e per unit of production)
   - Normalize emissions against business metrics
   - Measure operational efficiency improvements

3. **Emission Hotspot Analysis**
   - Identify highest-contributing emission sources
   - Prioritize reduction efforts
   - Analyze by activity type, scope, and time period

## Historical Accuracy Mechanism

When an emission record is created:
1. System queries for the emission factor valid on the activity date
2. Factor is selected using: `valid_from <= activity_date AND (valid_to >= activity_date OR valid_to IS NULL)`
3. The `factor_id` is permanently linked to the emission record
4. Even if factors are updated later, historical records remain unchanged

This "pyramid strategy" ensures all analytical insights are built on a foundation of trustworthy, auditable data.

## API Standards

- **RESTful design** - Standard HTTP methods and status codes
- **JSON responses** - All responses in JSON format
- **Error handling** - Standardized error responses with codes and details
- **Validation** - Comprehensive input validation using Pydantic
- **Performance** - Optimized SQL queries with proper indexing

## Authentication

Currently, the API is open for development. Production deployments should implement:
- API key authentication
- Rate limiting
- Role-based access control
    """,
    contact={
        "name": "Carbon Emissions Platform Team",
        "email": "support@ghgplatform.example.com"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    },
    openapi_tags=[
        {
            "name": "analytics",
            "description": "Advanced analytics and reporting endpoints for emission data analysis"
        },
        {
            "name": "health",
            "description": "System health and status endpoints"
        }
    ]
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register exception handlers
register_exception_handlers(app)

# Include routers
app.include_router(analytics.router)
app.include_router(emissions.router)
app.include_router(metrics.router)


@app.on_event("startup")
async def startup_event():
    """Initialize resources on application startup"""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    init_database()
    logger.info("Application startup complete")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on application shutdown"""
    logger.info("Shutting down application")
    close_database()
    logger.info("Application shutdown complete")


@app.get(
    "/health",
    tags=["health"],
    summary="Health Check",
    description="Check the health status of the application and database connection",
    response_description="Health status information"
)
async def health_check():
    """
    Health check endpoint for monitoring and load balancers.
    
    Returns the health status of:
    - Application service
    - Database connection
    - Configuration details
    
    Returns:
        dict: Health status with application and database information
        
    Status Codes:
        - 200: Service is healthy
        - 503: Service is unhealthy (database connection failed)
    """
    db_healthy = db_pool.health_check()
    
    return {
        "status": "healthy" if db_healthy else "unhealthy",
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "database": {
            "connected": db_healthy,
            "host": settings.DB_HOST,
            "database": settings.DB_NAME
        }
    }


@app.get(
    "/",
    tags=["health"],
    summary="Root Endpoint",
    description="Welcome endpoint with API information and documentation links"
)
async def root():
    """
    Root endpoint providing API information and navigation.
    
    Returns:
        dict: Welcome message with version and documentation links
    """
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "documentation": {
            "interactive_docs": "/docs",
            "openapi_spec": "/openapi.json",
            "redoc": "/redoc"
        },
        "endpoints": {
            "health": "/health",
            "analytics": "/api/analytics"
        }
    }
