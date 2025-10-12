"""
Emissions Router Module
Implements API endpoints for creating and managing emission records
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
    prefix="/api/emissions",
    tags=["emissions"],
    responses={
        500: {"description": "Internal server error"},
        400: {"description": "Bad request - invalid parameters"},
        404: {"description": "Resource not found"},
    }
)


class EmissionRequest(BaseModel):
    """Request model for creating an emission record"""
    activity_name: str = Field(..., description="Name of the emission activity")
    activity_value: float = Field(..., gt=0, description="Value of the activity")
    activity_unit: str = Field(..., description="Unit of measurement")
    activity_date: date = Field(..., description="Date of the activity")
    location: Optional[str] = Field(None, description="Location where activity occurred")
    department: Optional[str] = Field(None, description="Department responsible")
    notes: Optional[str] = Field(None, description="Additional notes")


class EmissionResponse(BaseModel):
    """Response model for emission record"""
    record_id: int
    activity_name: str
    activity_value: float
    activity_unit: str
    calculated_co2e: float
    scope: int
    activity_date: str
    message: str


@router.post(
    "/",
    response_model=EmissionResponse,
    summary="Create Emission Record",
    description="Create a new emission record with automatic CO2e calculation"
)
async def create_emission_record(
    emission: EmissionRequest = Body(...)
) -> EmissionResponse:
    """
    Create a new emission record.
    
    The system will:
    1. Find the appropriate emission factor valid on the activity date
    2. Calculate CO2e emissions automatically
    3. Store the record with permanent factor linkage
    
    Args:
        emission: Emission record data
        
    Returns:
        EmissionResponse: Created emission record with calculated CO2e
        
    Raises:
        HTTPException 400: If validation fails
        HTTPException 404: If no emission factor found
        HTTPException 500: If an unexpected error occurs
    """
    try:
        # Validate date is not in the future
        today = date.today()
        if emission.activity_date > today:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": "FUTURE_DATE",
                    "message": "Activity date cannot be in the future",
                    "details": {
                        "activity_date": emission.activity_date.isoformat(),
                        "today": today.isoformat()
                    }
                }
            )
        
        # Find the appropriate emission factor
        factor_query = """
            SELECT 
                factor_id,
                co2e_per_unit,
                activity_unit,
                scope
            FROM emission_factors
            WHERE activity_name = %s
              AND valid_from <= %s
              AND (valid_to >= %s OR valid_to IS NULL)
            ORDER BY valid_from DESC
            LIMIT 1
        """
        
        with get_db_cursor() as cursor:
            cursor.execute(
                factor_query,
                (emission.activity_name, emission.activity_date, emission.activity_date)
            )
            factor = cursor.fetchone()
            
            if not factor:
                raise HTTPException(
                    status_code=404,
                    detail={
                        "code": "FACTOR_NOT_FOUND",
                        "message": f"No emission factor found for '{emission.activity_name}' on {emission.activity_date}",
                        "details": {
                            "activity_name": emission.activity_name,
                            "activity_date": emission.activity_date.isoformat()
                        }
                    }
                )
            
            # Validate unit matches
            if emission.activity_unit != factor['activity_unit']:
                raise HTTPException(
                    status_code=400,
                    detail={
                        "code": "UNIT_MISMATCH",
                        "message": f"Unit mismatch: expected '{factor['activity_unit']}' but got '{emission.activity_unit}'",
                        "details": {
                            "expected_unit": factor['activity_unit'],
                            "provided_unit": emission.activity_unit
                        }
                    }
                )
            
            # Calculate CO2e
            calculated_co2e = emission.activity_value * float(factor['co2e_per_unit'])
            
            # Insert emission record
            insert_query = """
                INSERT INTO emission_records (
                    factor_id,
                    activity_date,
                    activity_name,
                    activity_value,
                    activity_unit,
                    calculated_co2e,
                    scope,
                    location,
                    department,
                    notes
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING record_id
            """
            
            cursor.execute(
                insert_query,
                (
                    factor['factor_id'],
                    emission.activity_date,
                    emission.activity_name,
                    emission.activity_value,
                    emission.activity_unit,
                    calculated_co2e,
                    factor['scope'],
                    emission.location,
                    emission.department,
                    emission.notes
                )
            )
            
            result = cursor.fetchone()
            record_id = result['record_id']
            
            # Commit the transaction
            cursor.connection.commit()
            
            logger.info(
                f"Created emission record {record_id}: {emission.activity_name} "
                f"({emission.activity_value} {emission.activity_unit}) = {calculated_co2e:.2f} kgCO2e"
            )
            
            return EmissionResponse(
                record_id=record_id,
                activity_name=emission.activity_name,
                activity_value=emission.activity_value,
                activity_unit=emission.activity_unit,
                calculated_co2e=calculated_co2e,
                scope=factor['scope'],
                activity_date=emission.activity_date.isoformat(),
                message=f"Emission record created successfully. Calculated {calculated_co2e:.2f} kgCO2e"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating emission record: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred while creating emission record",
                "details": {"error": str(e)}
            }
        )
