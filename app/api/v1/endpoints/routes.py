from fastapi import APIRouter, Depends, HTTPException, Query, status,UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app.core.logger.logging import get_logger
from app.core.models.pydantic_models import FeatureOut
from app.database.rds import get_db
from app.core.constants.exception_constants import ExceptionConstants
from app.core.constants.logger_constants import LoggerConstants
from app.services.feature_search_service import FeatureSearchService
from app.services.autocomplete_service import AutocompleteService
from app.services.geojson_upload_service import GeoJSONUploadService
import json


logger = get_logger()
router = APIRouter()


# Search features by full-text or similarity
@router.get("/search", response_model=List[FeatureOut], response_model_exclude_none=True)
def search_features(
    query: str = Query(..., min_length=1),
    filter: str = Query(None),
    db: Session = Depends(get_db)
):
    try:
        search_service = FeatureSearchService(db)
        return search_service.search_with_unified_filter(query, filter)
    except Exception as e:
        logger.error(f"{LoggerConstants.SEARCH_ERROR}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{ExceptionConstants.SEARCH_ERROR}: {str(e)}"
        )
# def search_features(
#     query: str = Query(..., min_length=1),
#     category: str = Query(None),
#     sub_category: str = Query(None),
#     db: Session = Depends(get_db)
# ):
#     try:
#         search_service = FeatureSearchService(db)
#         return search_service.search_with_filters(query, category, sub_category)
#     except Exception as e:
#         logger.error(f"{LoggerConstants.SEARCH_ERROR}: {str(e)}")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"{ExceptionConstants.SEARCH_ERROR}: {str(e)}"
#         )

# Autocomplete suggestions
@router.get("/autocomplete", response_model=List[str])
def autocomplete(query: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    try:
        autocomplete_service = AutocompleteService(db)
        return autocomplete_service.get_suggestions(query)
    except Exception as e:
        logger.error(f"{LoggerConstants.AUTOCOMPLETE_ERROR}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{ExceptionConstants.AUTOCOMPLETE_ERROR}: {str(e)}"
        )
# Add GeoJson
@router.post("/upload-geojson")
async def upload_geojson(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(".geojson") and not file.filename.endswith(".json"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ExceptionConstants.INVALID_FILE_TYPE
        )

    try:
        content = await file.read()
        data = json.loads(content)
    except Exception as e:
        logger.error(f"Failed to parse GeoJSON: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ExceptionConstants.INVALID_GEOJSON_FORMAT
        )

    service = GeoJSONUploadService(db)
    result = service.process_geojson(data)
    return {"message": f"{result} features processed."}