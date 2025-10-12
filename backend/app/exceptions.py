"""
Custom Exceptions and Error Handlers for Carbon Emissions Platform

This module defines custom exception classes and FastAPI exception handlers
to provide standardized error responses across the API.
"""
from typing import Any, Dict, Optional
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# Custom Exception Classes
# ============================================================================

class GHGPlatformException(Exception):
    """Base exception class for all GHG Platform custom exceptions"""
    
    def __init__(
        self,
        message: str,
        error_code: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class FactorNotFoundException(GHGPlatformException):
    """
    Exception raised when no emission factor is found for a given activity and date.
    
    This typically occurs when:
    - No emission factor exists for the specified activity name and scope
    - No factor is valid for the specified activity date
    - The factor has been retired and no replacement exists
    
    Requirements: 1.3 - Historical accuracy requires valid factors for all dates
    """
    
    def __init__(
        self,
        activity_name: str,
        scope: int,
        activity_date: str,
        details: Optional[Dict[str, Any]] = None
    ):
        error_details = {
            "activity_name": activity_name,
            "scope": scope,
            "activity_date": activity_date
        }
        if details:
            error_details.update(details)
        
        message = (
            f"No emission factor found for activity '{activity_name}' "
            f"(Scope {scope}) on date {activity_date}. "
            f"Please ensure a valid emission factor exists for this activity and date."
        )
        
        super().__init__(
            message=message,
            error_code="FACTOR_NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
            details=error_details
        )


class NoProductionDataException(GHGPlatformException):
    """
    Exception raised when production/business metric data is not available.
    
    This occurs when calculating emission intensity and:
    - No business metric records exist for the specified period
    - The total production value is zero
    - The specified metric name doesn't exist
    
    Requirements: 3.5 - Intensity calculation requires production data
    """
    
    def __init__(
        self,
        metric_name: str,
        start_date: str,
        end_date: str,
        details: Optional[Dict[str, Any]] = None
    ):
        error_details = {
            "metric_name": metric_name,
            "start_date": start_date,
            "end_date": end_date
        }
        if details:
            error_details.update(details)
        
        message = (
            f"No production data found for metric '{metric_name}' "
            f"in the period from {start_date} to {end_date}. "
            f"Emission intensity cannot be calculated without production data."
        )
        
        super().__init__(
            message=message,
            error_code="NO_PRODUCTION_DATA",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=error_details
        )


class InvalidDateRangeException(GHGPlatformException):
    """
    Exception raised when an invalid date range is provided.
    
    This occurs when:
    - End date is before start date
    - Date range is too large (exceeds maximum allowed period)
    - Dates are in an invalid format
    - Future dates are provided where not allowed
    
    Requirements: 4.1 - API endpoints must validate input parameters
    """
    
    def __init__(
        self,
        start_date: str,
        end_date: str,
        reason: str,
        details: Optional[Dict[str, Any]] = None
    ):
        error_details = {
            "start_date": start_date,
            "end_date": end_date,
            "reason": reason
        }
        if details:
            error_details.update(details)
        
        message = (
            f"Invalid date range: {reason}. "
            f"Start date: {start_date}, End date: {end_date}"
        )
        
        super().__init__(
            message=message,
            error_code="INVALID_DATE_RANGE",
            status_code=status.HTTP_400_BAD_REQUEST,
            details=error_details
        )


class DatabaseConnectionException(GHGPlatformException):
    """
    Exception raised when database connection or query fails.
    """
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=f"Database error: {message}",
            error_code="DATABASE_ERROR",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            details=details or {}
        )


class InvalidScopeException(GHGPlatformException):
    """
    Exception raised when an invalid emission scope is provided.
    
    Valid scopes are 1, 2, or 3 according to GHG Protocol.
    """
    
    def __init__(self, scope: Any, details: Optional[Dict[str, Any]] = None):
        error_details = {"provided_scope": scope, "valid_scopes": [1, 2, 3]}
        if details:
            error_details.update(details)
        
        message = (
            f"Invalid scope value: {scope}. "
            f"Scope must be 1 (Direct), 2 (Indirect - Energy), or 3 (Indirect - Other)."
        )
        
        super().__init__(
            message=message,
            error_code="INVALID_SCOPE",
            status_code=status.HTTP_400_BAD_REQUEST,
            details=error_details
        )


# ============================================================================
# Error Response Formatter
# ============================================================================

def format_error_response(
    error_code: str,
    message: str,
    details: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create a standardized error response format.
    
    Args:
        error_code: Machine-readable error code
        message: Human-readable error message
        details: Additional context about the error
    
    Returns:
        Standardized error response dictionary
    """
    return {
        "error": {
            "code": error_code,
            "message": message,
            "details": details or {}
        }
    }


# ============================================================================
# FastAPI Exception Handlers
# ============================================================================

async def ghg_platform_exception_handler(
    request: Request,
    exc: GHGPlatformException
) -> JSONResponse:
    """
    Handler for all custom GHG Platform exceptions.
    
    Converts custom exceptions into standardized JSON error responses.
    """
    logger.warning(
        f"GHG Platform Exception: {exc.error_code} - {exc.message}",
        extra={"details": exc.details, "path": request.url.path}
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=format_error_response(
            error_code=exc.error_code,
            message=exc.message,
            details=exc.details
        )
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
) -> JSONResponse:
    """
    Handler for Pydantic validation errors.
    
    Converts validation errors into standardized format.
    """
    logger.warning(
        f"Validation error on {request.url.path}",
        extra={"errors": exc.errors()}
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=format_error_response(
            error_code="VALIDATION_ERROR",
            message="Request validation failed",
            details={
                "validation_errors": exc.errors(),
                "body": exc.body if hasattr(exc, 'body') else None
            }
        )
    )


async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException
) -> JSONResponse:
    """
    Handler for standard HTTP exceptions.
    
    Converts HTTP exceptions into standardized format.
    """
    logger.warning(
        f"HTTP {exc.status_code} on {request.url.path}: {exc.detail}"
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=format_error_response(
            error_code=f"HTTP_{exc.status_code}",
            message=str(exc.detail),
            details={"status_code": exc.status_code}
        )
    )


async def unhandled_exception_handler(
    request: Request,
    exc: Exception
) -> JSONResponse:
    """
    Handler for unexpected/unhandled exceptions.
    
    Logs the full exception and returns a generic error response
    to avoid exposing internal details.
    """
    logger.error(
        f"Unhandled exception on {request.url.path}: {str(exc)}",
        exc_info=True,
        extra={"path": request.url.path, "method": request.method}
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=format_error_response(
            error_code="INTERNAL_SERVER_ERROR",
            message="An unexpected error occurred. Please try again later.",
            details={
                "path": request.url.path,
                "method": request.method
            }
        )
    )


# ============================================================================
# Exception Handler Registration Function
# ============================================================================

def register_exception_handlers(app):
    """
    Register all custom exception handlers with the FastAPI application.
    
    This should be called during application initialization.
    
    Args:
        app: FastAPI application instance
    """
    # Custom GHG Platform exceptions
    app.add_exception_handler(GHGPlatformException, ghg_platform_exception_handler)
    
    # Validation errors
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    
    # HTTP exceptions
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    
    # Catch-all for unhandled exceptions
    app.add_exception_handler(Exception, unhandled_exception_handler)
    
    logger.info("Exception handlers registered successfully")
