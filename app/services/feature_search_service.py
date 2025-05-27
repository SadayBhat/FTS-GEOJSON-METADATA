from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.dao.geo_feature_dao import GeoFeatureDAO
from app.services.feature_conversion_service import FeatureConversionService
from loguru import logger


class FeatureSearchService:

    def __init__(self, db: Session):
        self.db = db
        self.dao = GeoFeatureDAO(db)
        self.logger = logger.bind(name="FeatureSearchService")

    def search_by_query(self, query: str):
        try:
            results = self.dao.search_by_text(query)
            if not results:
                self.logger.info(f"No results for '{query}' in full-text. Trying similarity...")
                results = self.dao.search_by_similarity(query)

            return [FeatureConversionService.convert(f) for f in results]
        except Exception as e:
            self.logger.error(f"Search error: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
