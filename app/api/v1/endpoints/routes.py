from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List

from app.core.logger.logging import get_logger
from app.core.models.pydantic_models import FeatureOut
from app.database.rds import get_db
from app.core.constants.exception_constants import ExceptionConstants

from app.services.feature_search_service import FeatureSearchService
from app.services.spatial_search_service import SpatialSearchService
from app.services.autocomplete_service import AutocompleteService

logger = get_logger()
router = APIRouter()


# Search features by full-text or similarity
@router.get("/search", response_model=List[FeatureOut], response_model_exclude_none=True)
def search_features(query: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    try:
        search_service = FeatureSearchService(db)
        return search_service.search_by_query(query)
    except Exception as e:
        logger.error(f"Error during search: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{ExceptionConstants.SEARCH_ERROR}: {str(e)}"
        )


# Search railways within a radius
@router.get("/search/railways", response_model=List[FeatureOut], response_model_exclude_none=True)
def get_railway(lat: float, lon: float, radius_km: float = 20.0, db: Session = Depends(get_db)):
    try:
        spatial_search_service = SpatialSearchService(db)
        return spatial_search_service.search_railways(lat, lon, radius_km)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error during railway search: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{ExceptionConstants.RAILWAY_SEARCH_ERROR}: {str(e)}"
        )


# Search features within bounding box
@router.get("/search/bbox", response_model=List[FeatureOut])
def search_bbox(min_lat: float, min_lon: float, max_lat: float, max_lon: float, db: Session = Depends(get_db)):
    try:
        spatial_search_service = SpatialSearchService(db)
        return spatial_search_service.search_bbox(min_lat, min_lon, max_lat, max_lon)
    except Exception as e:
        logger.error(f"Error during bbox search: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{ExceptionConstants.BBOX_SEARCH_ERROR}: {str(e)}"
        )


# Search features within buffer zone
@router.get("/search/buffer", response_model=List[FeatureOut])
def search_buffer(lat: float, lon: float, buffer_km: float = 5.0, db: Session = Depends(get_db)):
    try:
        spatial_search_service = SpatialSearchService(db)
        return spatial_search_service.search_buffer(lat, lon, buffer_km)
    except Exception as e:
        logger.error(f"Error during buffer search: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{ExceptionConstants.BUFFER_SEARCH_ERROR}: {str(e)}"
        )


# Autocomplete suggestions
@router.get("/autocomplete", response_model=List[str])
def autocomplete(query: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    try:
        autocomplete_service = AutocompleteService(db)
        return autocomplete_service.get_suggestions(query)
    except Exception as e:
        logger.error(f"Error during autocomplete: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{ExceptionConstants.AUTOCOMPLETE_ERROR}: {str(e)}"
        )
