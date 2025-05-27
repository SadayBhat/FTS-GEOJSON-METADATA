from pydantic import BaseModel, Field
from typing import Optional, Any, List, Dict

class GeometrySchema(BaseModel):
    """GeoJSON Geometry Schema"""
    type: str
    coordinates: List[Any]

class FeatureProperties(BaseModel):
    """Feature Properties Schema"""
    name: Optional[str] = None
    category: Optional[str] = None
    railway: Optional[str] = None
    source: Optional[str] = None
    sub_category: Optional[str] = None
    highway: Optional[str] = None
    geohash_id: Optional[str] = None
    type: Optional[str] = None

class FeatureOut(BaseModel):
    """Feature Output Schema"""
    type: str
    properties: Dict[str, Any]
    geometry: GeometrySchema
    distance_Km: Optional[float] = None

    class Config:
        from_attributes = True
        populate_by_name = True

class SearchRequest(BaseModel):
    """Search Request Schema"""
    query: str = Field(..., min_length=1, description="Search query string")
    limit: Optional[int] = Field(20, ge=1, le=100, description="Maximum number of results")

class LocationRequest(BaseModel):
    """Location-based Request Schema"""
    lat: float = Field(..., ge=-90, le=90, description="Latitude")
    lon: float = Field(..., ge=-180, le=180, description="Longitude")
    radius_km: Optional[float] = Field(20.0, gt=0, description="Search radius in kilometers")

class BBoxRequest(BaseModel):
    """Bounding Box Request Schema"""
    min_lat: float = Field(..., ge=-90, le=90, description="Minimum latitude")
    min_lon: float = Field(..., ge=-180, le=180, description="Minimum longitude")
    max_lat: float = Field(..., ge=-90, le=90, description="Maximum latitude")
    max_lon: float = Field(..., ge=-180, le=180, description="Maximum longitude")
