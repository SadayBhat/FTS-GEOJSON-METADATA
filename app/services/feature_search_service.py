from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.dao.geo_feature_dao import GeoFeatureDAO
from loguru import logger
from app.core.models.pydantic_models import FeatureOut


class FeatureSearchService:

    def __init__(self, db: Session):
        self.db = db
        self.dao = GeoFeatureDAO(db)
        self.logger = logger.bind(name="FeatureSearchService")

    def search_by_query(self, query: str):
        try:
            self.logger.debug(f"Performing full-text search for query: {query}")
            results = self.dao.search_by_text(query)

            if not results:
                self.logger.info(f"No full-text results for '{query}'. Trying similarity...")
                results = self.dao.search_by_similarity(query)

            self.logger.debug(f"Found {len(results)} total results for query: {query}")
            
            # Ensure that results are converted into FeatureOut before returning
            return [FeatureOut.from_orm(result) for result in results]

        except Exception as e:
            self.logger.error(f"Search error: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
    # def search_with_filters(self, query: str, category: str = None, sub_category: str = None):
    #     return self.dao.search_by_filters(query, category, sub_category)

    def search_with_unified_filter(self, query: str, filter: str = None):
        return self.dao.search_by_unified_filter(query, filter)

