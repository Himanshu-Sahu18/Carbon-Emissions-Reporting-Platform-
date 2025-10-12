"""
Pydantic models for request/response validation.
"""
from .requests import EmissionIntensityRequest, HotspotFilters
from .responses import (
    ScopeEmission,
    YoYResponse,
    EmissionIntensityResponse,
    HotspotItem,
    HotspotsResponse,
)

__all__ = [
    # Request models
    "EmissionIntensityRequest",
    "HotspotFilters",
    # Response models
    "ScopeEmission",
    "YoYResponse",
    "EmissionIntensityResponse",
    "HotspotItem",
    "HotspotsResponse",
]
