from app.dao.geo_feature_dao import GeoFeatureDAO
from sqlalchemy.orm import Session
from loguru import logger


class AutocompleteService:

    def __init__(self, db: Session):
        self.dao = GeoFeatureDAO(db)
        self.logger = logger.bind(name="AutocompleteService")

    def get_suggestions(self, query: str):
        try:
            return self.dao.get_autocomplete_suggestions(query)
        except Exception as e:
            self.logger.error(f"Autocomplete error: {str(e)}")
            raise
