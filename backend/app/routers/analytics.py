"""
Analytics Router Module
Implements API endpoints for analytics and reporting features
"""
import logging
from datetime import date, datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, Query, Depends

from app.services.analytics_service import AnalyticsService
from app.repositories.emission_repository import EmissionRepository
from app.repositories.business_metrics_repository import BusinessMetricsRepository
from app.models.responses import YoYResponse, EmissionIntensityResponse, HotspotsResponse

logger = logging.getLogger(__name__)

# Create router instance
router = APIRouter(
    prefix="/api/analytics",
    tags=["analytics"],
    responses={
        500: {"description": "Internal server error"},
        400: {"description": "Bad request - invalid parameters"},
        404: {"description": "Resource not found"},
        422: {"description": "Unprocessable entity - business logic error"}
    }
)


# Dependency injection for AnalyticsService
def get_analytics_service() -> AnalyticsService:
    """
    Dependency injection function for AnalyticsService.
    Creates service instance with repository dependencies.
    
    Returns:
        AnalyticsService: Configured analytics service instance
    """
    emission_repo = EmissionRepository()
    business_metrics_repo = BusinessMetricsRepository()
    return AnalyticsService(
        emission_repository=emission_repo,
        business_metrics_repository=business_metrics_repo
    )



@router.get(
    "/yoy",
    response_model=YoYResponse,
    summary="Year-over-Year Emissions Comparison",
    description="Compare total emissions by scope between current year and previous year"
)
async def get_yoy_emissions(
    current_year: Optional[int] = Query(
        default=None,
        description="Current year to analyze (defaults to current year)"
    ),
    previous_year: Optional[int] = Query(
        default=None,
        description="Previous year for comparison (defaults to current_year - 1)"
    ),
    analytics_service: AnalyticsService = Depends(get_analytics_service)
) -> YoYResponse:
    """
    Retrieve Year-over-Year emissions comparison grouped by scope.
    
    This endpoint compares total emissions between two years, showing:
    - Emissions by scope (1, 2, 3) for both years
    - Total emissions for each year
    - Percentage and absolute change between years
    
    Args:
        current_year: Year to analyze (defaults to current year)
        previous_year: Year for comparison (defaults to current_year - 1)
        analytics_service: Injected analytics service
        
    Returns:
        YoYResponse: Year-over-year comparison data
        
    Raises:
        HTTPException 400: If year parameters are invalid
        HTTPException 500: If an unexpected error occurs
        
    Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7
    """
    try:
        # Set default years if not provided
        if current_year is None:
            current_year = datetime.now().year
        
        if previous_year is None:
            previous_year = current_year - 1
        
        # Validate year parameters
        if current_year < 1900 or current_year > 2100:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": "INVALID_YEAR",
                    "message": f"Current year {current_year} is out of valid range (1900-2100)",
                    "details": {"current_year": current_year}
                }
            )
        
        if previous_year < 1900 or previous_year > 2100:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": "INVALID_YEAR",
                    "message": f"Previous year {previous_year} is out of valid range (1900-2100)",
                    "details": {"previous_year": previous_year}
                }
            )
        
        if previous_year >= current_year:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": "INVALID_YEAR_RANGE",
                    "message": "Previous year must be before current year",
                    "details": {
                        "current_year": current_year,
                        "previous_year": previous_year
                    }
                }
            )
        
        logger.info(f"YoY API called: current_year={current_year}, previous_year={previous_year}")
        
        # Call service to get YoY data
        result = analytics_service.get_yoy_emissions(
            current_year=current_year,
            previous_year=previous_year
        )
        
        return YoYResponse(**result)
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error in YoY API endpoint: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred while processing YoY emissions",
                "details": {"error": str(e)}
            }
        )



@router.get(
    "/intensity",
    response_model=EmissionIntensityResponse,
    summary="Emission Intensity Calculation",
    description="Calculate carbon efficiency as kgCO₂e per unit of production for a given period"
)
async def get_emission_intensity(
    start_date: date = Query(
        ...,
        description="Start date of the period (YYYY-MM-DD)"
    ),
    end_date: date = Query(
        ...,
        description="End date of the period (YYYY-MM-DD)"
    ),
    metric_name: str = Query(
        ...,
        description="Business metric to use for intensity calculation (e.g., 'Tons of Steel Produced')"
    ),
    analytics_service: AnalyticsService = Depends(get_analytics_service)
) -> EmissionIntensityResponse:
    """
    Calculate emission intensity (kgCO₂e per unit of production) for a period.
    
    This endpoint calculates carbon efficiency by dividing total emissions
    by total production for a specified business metric and date range.
    
    Args:
        start_date: Start of the period
        end_date: End of the period
        metric_name: Name of the business metric (e.g., 'Tons of Steel Produced')
        analytics_service: Injected analytics service
        
    Returns:
        EmissionIntensityResponse: Emission intensity data
        
    Raises:
        HTTPException 400: If date range is invalid
        HTTPException 404: If metric not found
        HTTPException 422: If production data is zero or missing (division by zero)
        HTTPException 500: If an unexpected error occurs
        
    Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7
    """
    try:
        # Validate date range
        if end_date < start_date:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": "INVALID_DATE_RANGE",
                    "message": "end_date must be after start_date",
                    "details": {
                        "start_date": start_date.isoformat(),
                        "end_date": end_date.isoformat()
                    }
                }
            )
        
        # Validate date range is not too large (max 10 years for performance)
        date_diff = (end_date - start_date).days
        if date_diff > 3650:  # ~10 years
            raise HTTPException(
                status_code=400,
                detail={
                    "code": "DATE_RANGE_TOO_LARGE",
                    "message": "Date range cannot exceed 10 years",
                    "details": {
                        "start_date": start_date.isoformat(),
                        "end_date": end_date.isoformat(),
                        "days": date_diff
                    }
                }
            )
        
        # Validate metric_name is not empty
        if not metric_name or not metric_name.strip():
            raise HTTPException(
                status_code=400,
                detail={
                    "code": "INVALID_METRIC_NAME",
                    "message": "metric_name cannot be empty",
                    "details": {}
                }
            )
        
        logger.info(
            f"Intensity API called: start_date={start_date}, end_date={end_date}, "
            f"metric_name='{metric_name}'"
        )
        
        # Call service to calculate intensity
        result = analytics_service.calculate_emission_intensity(
            start_date=start_date,
            end_date=end_date,
            metric_name=metric_name.strip()
        )
        
        return EmissionIntensityResponse(**result)
        
    except ValueError as e:
        # Handle division by zero and missing production data
        error_message = str(e)
        
        if "No production data found" in error_message or "Total production is zero" in error_message:
            logger.warning(f"No production data for intensity calculation: {e}")
            raise HTTPException(
                status_code=422,
                detail={
                    "code": "INTENSITY_NO_PRODUCTION_DATA",
                    "message": error_message,
                    "details": {
                        "metric_name": metric_name,
                        "start_date": start_date.isoformat(),
                        "end_date": end_date.isoformat()
                    }
                }
            )
        else:
            # Other ValueError cases
            logger.error(f"Validation error in intensity calculation: {e}")
            raise HTTPException(
                status_code=400,
                detail={
                    "code": "VALIDATION_ERROR",
                    "message": error_message,
                    "details": {}
                }
            )
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error in Intensity API endpoint: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred while calculating emission intensity",
                "details": {"error": str(e)}
            }
        )



@router.get(
    "/hotspots",
    response_model=HotspotsResponse,
    summary="Emission Hotspot Analysis",
    description="Identify which emission sources contribute the most to total footprint"
)
async def get_emission_hotspots(
    start_date: Optional[date] = Query(
        default=None,
        description="Filter start date (YYYY-MM-DD)"
    ),
    end_date: Optional[date] = Query(
        default=None,
        description="Filter end date (YYYY-MM-DD)"
    ),
    scope: Optional[int] = Query(
        default=None,
        ge=1,
        le=3,
        description="Filter by emission scope (1, 2, or 3)"
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Maximum number of hotspots to return"
    ),
    analytics_service: AnalyticsService = Depends(get_analytics_service)
) -> HotspotsResponse:
    """
    Identify emission hotspots by analyzing top emission sources.
    
    This endpoint returns the highest-contributing emission sources,
    sorted by total emissions in descending order, with percentage
    contributions calculated relative to total emissions.
    
    Args:
        start_date: Optional filter for start date
        end_date: Optional filter for end date
        scope: Optional filter for emission scope (1, 2, or 3)
        limit: Maximum number of hotspots to return (1-100, default 10)
        analytics_service: Injected analytics service
        
    Returns:
        HotspotsResponse: Emission hotspot analysis data
        
    Raises:
        HTTPException 400: If filters are invalid
        HTTPException 500: If an unexpected error occurs
        
    Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8
    """
    try:
        # Validate date range if both dates provided
        if start_date and end_date and end_date < start_date:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": "INVALID_DATE_RANGE",
                    "message": "end_date must be after start_date",
                    "details": {
                        "start_date": start_date.isoformat(),
                        "end_date": end_date.isoformat()
                    }
                }
            )
        
        # Validate date range is not too large if both dates provided
        if start_date and end_date:
            date_diff = (end_date - start_date).days
            if date_diff > 3650:  # ~10 years
                raise HTTPException(
                    status_code=400,
                    detail={
                        "code": "DATE_RANGE_TOO_LARGE",
                        "message": "Date range cannot exceed 10 years",
                        "details": {
                            "start_date": start_date.isoformat(),
                            "end_date": end_date.isoformat(),
                            "days": date_diff
                        }
                    }
                )
        
        # Build filters dictionary
        filters = {
            "start_date": start_date,
            "end_date": end_date,
            "scope": scope,
            "limit": limit
        }
        
        logger.info(f"Hotspots API called with filters: {filters}")
        
        # Call service to get hotspot data
        result = analytics_service.get_emission_hotspots(filters=filters)
        
        return HotspotsResponse(**result)
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error in Hotspots API endpoint: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred while analyzing emission hotspots",
                "details": {"error": str(e)}
            }
        )


@router.get(
    "/monthly",
    summary="Monthly Emissions Trend",
    description="Get monthly emissions aggregated by month for a given year"
)
async def get_monthly_emissions(
    year: int = Query(
        default=2024,
        ge=2000,
        le=2100,
        description="Year to get monthly emissions for"
    ),
    analytics_service: AnalyticsService = Depends(get_analytics_service)
):
    """
    Get monthly emissions trend for a specific year.
    
    Returns emissions aggregated by month, useful for trend analysis.
    
    Args:
        year: Year to analyze (2000-2100)
        analytics_service: Injected analytics service
        
    Returns:
        dict: Monthly emissions data with months and totals
        
    Raises:
        HTTPException 500: If an unexpected error occurs
    """
    try:
        logger.info(f"Monthly emissions API called for year: {year}")
        
        # Get monthly data from repository
        emission_repo = EmissionRepository()
        monthly_data = emission_repo.get_monthly_emissions(year)
        
        return {
            "year": year,
            "monthly_data": monthly_data
        }
        
    except Exception as e:
        logger.error(f"Error in Monthly Emissions API endpoint: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred while fetching monthly emissions",
                "details": {"error": str(e)}
            }
        )
