"""
Request models for the Analytics API endpoints.
"""
from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class EmissionIntensityRequest(BaseModel):
    """Request model for emission intensity calculation."""
    start_date: date
    end_date: date
    metric_name: str

    @field_validator('end_date')
    @classmethod
    def end_after_start(cls, v: date, info) -> date:
        """Validate that end_date is after start_date."""
        if 'start_date' in info.data and v < info.data['start_date']:
            raise ValueError('end_date must be after start_date')
        return v

    @field_validator('metric_name')
    @classmethod
    def metric_name_not_empty(cls, v: str) -> str:
        """Validate that metric_name is not empty."""
        if not v or not v.strip():
            raise ValueError('metric_name cannot be empty')
        return v.strip()


class HotspotFilters(BaseModel):
    """Request model for emission hotspot filtering."""
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    scope: Optional[int] = Field(None, ge=1, le=3, description="Emission scope (1, 2, or 3)")
    limit: int = Field(10, ge=1, le=100, description="Maximum number of hotspots to return")

    @field_validator('end_date')
    @classmethod
    def end_after_start(cls, v: Optional[date], info) -> Optional[date]:
        """Validate that end_date is after start_date if both are provided."""
        if v is not None and 'start_date' in info.data and info.data['start_date'] is not None:
            if v < info.data['start_date']:
                raise ValueError('end_date must be after start_date')
        return v
