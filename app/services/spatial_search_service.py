from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.dao.geo_feature_dao import GeoFeatureDAO
from app.services.feature_conversion_service import FeatureConversionService
from app.core.constants.response_constants import ResponseConstants
from app.core.constants.app_constants import AppConstants
from loguru import logger


class SpatialSearchService:

    def __init__(self, db: Session):
        self.db = db
        self.dao = GeoFeatureDAO(db)
        self.logger = logger.bind(name="SpatialSearchService")

    def search_railways(self, lat: float, lon: float, radius_km: float):
        try:
            railways = self.dao.search_railways_by_location(lat, lon, radius_km)
            if not railways:
                raise HTTPException(status_code=404, detail=f"{ResponseConstants.RAILWAY_NOT_FOUND} {radius_km} km of ({lat}, {lon})")

            result = []
            for railway, dist_m in railways:
                distance_km = round(float(dist_m) / AppConstants.METERS_PER_KM, 2)
                if distance_km <= radius_km:
                    feature_out = FeatureConversionService.convert(railway)
                    feature_out.distance_Km = distance_km
                    result.append(feature_out)

            if not result:
                raise HTTPException(status_code=404, detail=f"{ResponseConstants.RAILWAY_NOT_FOUND} within final check")

            return result
        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Error in search_railways: {str(e)}")
            raise

    def search_bbox(self, min_lat: float, min_lon: float, max_lat: float, max_lon: float):
        try:
            results = self.dao.search_by_bbox(min_lat, min_lon, max_lat, max_lon)
            if not results:
                raise HTTPException(status_code=404, detail=ResponseConstants.BBOX_NOT_FOUND)
            return [FeatureConversionService.convert(f) for f in results]
        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Error in search_bbox: {str(e)}")
            raise

    def search_buffer(self, lat: float, lon: float, buffer_km: float):
        try:
            results = self.dao.search_by_buffer(lat, lon, buffer_km)
            if not results:
                raise HTTPException(status_code=404, detail=ResponseConstants.BUFFER_NOT_FOUND)
            return [FeatureConversionService.convert(f) for f in results]
        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Error in search_buffer: {str(e)}")
            raise
