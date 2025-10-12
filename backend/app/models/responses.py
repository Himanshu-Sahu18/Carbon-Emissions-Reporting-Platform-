"""
Response models for the Analytics API endpoints.
"""
from typing import List, Dict, Any
from pydantic import BaseModel, Field


class ScopeEmission(BaseModel):
    """Model for emissions data grouped by scope."""
    scope: int = Field(..., ge=1, le=3, description="Emission scope (1, 2, or 3)")
    total_emissions: float = Field(..., description="Total emissions in kgCO2e")
    unit: str = Field(default="kgCO2e", description="Unit of measurement")


class YoYResponse(BaseModel):
    """Response model for Year-over-Year emissions comparison."""
    current_year: int = Field(..., description="Current year being analyzed")
    previous_year: int = Field(..., description="Previous year for comparison")
    current_year_data: List[ScopeEmission] = Field(
        default_factory=list,
        description="Emissions data for current year by scope"
    )
    previous_year_data: List[ScopeEmission] = Field(
        default_factory=list,
        description="Emissions data for previous year by scope"
    )
    comparison: Dict[str, Any] = Field(
        default_factory=dict,
        description="Comparison metrics between years"
    )


class EmissionIntensityResponse(BaseModel):
    """Response model for emission intensity calculation."""
    period: Dict[str, str] = Field(..., description="Date range for the calculation")
    metric_name: str = Field(..., description="Business metric used for intensity calculation")
    total_emissions: float = Field(..., description="Total emissions in kgCO2e")
    total_production: float = Field(..., description="Total production value")
    production_unit: str = Field(..., description="Unit of production metric")
    intensity: float = Field(..., description="Emission intensity (kgCO2e per unit)")
    intensity_unit: str = Field(..., description="Unit of intensity measurement")
    record_count: int = Field(..., description="Number of emission records included")


class HotspotItem(BaseModel):
    """Model for individual emission hotspot."""
    activity_name: str = Field(..., description="Name of the emission activity")
    scope: int = Field(..., ge=1, le=3, description="Emission scope (1, 2, or 3)")
    total_emissions: float = Field(..., description="Total emissions from this source in kgCO2e")
    percentage: float = Field(..., description="Percentage contribution to total emissions")
    record_count: int = Field(..., description="Number of emission records for this source")
    average_per_record: float = Field(..., description="Average emissions per record in kgCO2e")


class HotspotsResponse(BaseModel):
    """Response model for emission hotspot analysis."""
    period: Dict[str, Any] = Field(..., description="Date range and filters applied")
    total_emissions: float = Field(..., description="Total emissions across all sources in kgCO2e")
    hotspots: List[HotspotItem] = Field(
        default_factory=list,
        description="List of emission hotspots sorted by total emissions"
    )
