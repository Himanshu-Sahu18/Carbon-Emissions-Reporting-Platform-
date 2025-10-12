"""
Business Metrics Router Module
Implements API endpoints for creating and managing business metrics
"""
import logging
from datetime import date
from typing import Optional
from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel, Field

from app.database import get_db_cursor

logger = logging.getLogger(__name__)

# Create router instance
router = APIRouter(
    prefix="/api/metrics",
    tags=["metrics"],
    responses={
        500: {"description": "Internal server error"},
        400: {"description": "Bad request - invalid parameters"},
    }
)


class MetricRequest(BaseModel):
    """Request model for creating a business metric"""
    metric_name: str = Field(..., description="Name of the metric")
    value: float = Field(..., gt=0, description="Metric value")
    unit: str = Field(..., description="Unit of measurement")
    metric_date: date = Field(..., description="Date of the metric")
    notes: Optional[str] = Field(None, description="Additional notes")


class MetricResponse(BaseModel):
    """Response model for business metric"""
    metric_id: int
    metric_name: str
    value: float
    unit: str
    metric_date: str
    message: str


@router.post(
    "/",
    response_model=MetricResponse,
    summary="Create Business Metric",
    description="Create a new business metric record"
)
async def create_business_metric(
    metric: MetricRequest = Body(...)
) -> MetricResponse:
    """
    Create a new business metric record.
    
    Business metrics are used for calculating emission intensity
    (e.g., emissions per unit of production).
    
    Args:
        metric: Business metric data
        
    Returns:
        MetricResponse: Created business metric
        
    Raises:
        HTTPException 400: If validation fails
        HTTPException 500: If an unexpected error occurs
    """
    try:
        # Validate date is not in the future
        today = date.today()
        if metric.metric_date > today:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": "FUTURE_DATE",
                    "message": "Metric date cannot be in the future",
                    "details": {
                        "metric_date": metric.metric_date.isoformat(),
                        "today": today.isoformat()
                    }
                }
            )
        
        # Insert business metric
        insert_query = """
            INSERT INTO business_metrics (
                metric_name,
                value,
                unit,
                metric_date,
                notes
            ) VALUES (%s, %s, %s, %s, %s)
            RETURNING metric_id
        """
        
        with get_db_cursor() as cursor:
            cursor.execute(
                insert_query,
                (
                    metric.metric_name,
                    metric.value,
                    metric.unit,
                    metric.metric_date,
                    metric.notes
                )
            )
            
            result = cursor.fetchone()
            metric_id = result['metric_id']
            
            # Commit the transaction
            cursor.connection.commit()
            
            logger.info(
                f"Created business metric {metric_id}: {metric.metric_name} "
                f"= {metric.value} {metric.unit} on {metric.metric_date}"
            )
            
            return MetricResponse(
                metric_id=metric_id,
                metric_name=metric.metric_name,
                value=metric.value,
                unit=metric.unit,
                metric_date=metric.metric_date.isoformat(),
                message=f"Business metric created successfully"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating business metric: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred while creating business metric",
                "details": {"error": str(e)}
            }
        )
