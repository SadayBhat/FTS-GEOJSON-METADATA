from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.dao.geo_feature_dao import GeoFeatureDAO
from app.core.constants.exception_constants import ExceptionConstants
from app.core.logger.logging import get_logger

logger = get_logger()


class GeoJSONUploadService:
    def __init__(self, db: Session):
        self.db = db
        self.dao = GeoFeatureDAO(db)

    def process_geojson(self, data: dict) -> int:
        if "features" not in data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ExceptionConstants.MISSING_FEATURES
            )

        count = 0
        for feature in data["features"]:
            properties = feature.get("properties", {})
            geohash_id = properties.get("geohash_id")

            if not geohash_id:
                logger.warning("Skipping feature with missing geohash_id")
                continue

            self.dao.upsert_feature(properties)
            count += 1

        logger.info(f"Successfully processed {count} features")
        return count
