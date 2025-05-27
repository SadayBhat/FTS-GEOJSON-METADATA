from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from geoalchemy2 import Geography
from loguru import logger

from app.database.models import GeoFeature
from app.core.constants.app_constants import AppConstants
from app.core.config import settings

class GeoFeatureDAO:
    """Data Access Object for GeoFeature operations"""
    
    def __init__(self, db: Session):
        self.db = db
        self.logger = logger.bind(name="GeoFeatureDAO")
    
    def search_by_text(self, query: str, limit: int = None) -> List[GeoFeature]:
        """
        Search features using full-text search
        """
        if limit is None:
            limit = settings.DEFAULT_SEARCH_LIMIT
            
        try:
            # Full-text search using PostgreSQL's plainto_tsquery
            ts_query = func.plainto_tsquery('english', query)
            results = (
                self.db.query(GeoFeature)
                .filter(GeoFeature.search_vector.op("@@")(ts_query))
                .limit(limit)
                .all()
            )
            
            self.logger.debug(f"Full-text search found {len(results)} results")
            return results
            
        except Exception as e:
            self.logger.error(f"Error in full-text search: {str(e)}")
            raise
    
    def search_by_similarity(self, query: str, limit: int = None) -> List[GeoFeature]:
        """
        Search features using similarity matching
        """
        if limit is None:
            limit = settings.DEFAULT_SEARCH_LIMIT
            
        try:
            similarity_threshold = settings.SIMILARITY_THRESHOLD
            sim_name = func.word_similarity(GeoFeature.properties["name"].astext, query)
            sim_project = func.word_similarity(GeoFeature.properties["project"].astext, query)
            
            results = (
                self.db.query(GeoFeature)
                .filter(
                    (sim_name >= similarity_threshold) |
                    (sim_project >= similarity_threshold) |
                    GeoFeature.properties["name"].astext.ilike(f"%{query}%") |
                    GeoFeature.properties["project"].astext.ilike(f"%{query}%")
                )
                .order_by(func.greatest(sim_name, sim_project).desc())
                .limit(limit)
                .all()
            )
            
            self.logger.debug(f"Similarity search found {len(results)} results")
            return results
            
        except Exception as e:
            self.logger.error(f"Error in similarity search: {str(e)}")
            raise
    
    def search_railways_by_location(
        self, 
        lat: float, 
        lon: float, 
        radius_km: float
    ) -> List[Tuple[GeoFeature, float]]:
        """
        Search railway stations within specified radius
        """
        try:
            user_location_geog = func.ST_SetSRID(
                func.ST_MakePoint(lon, lat), 
                AppConstants.SRID_WGS84
            ).cast(Geography)
            
            railways = (
                self.db.query(
                    GeoFeature,
                    func.ST_Distance(GeoFeature.geometry, user_location_geog).label("distance")
                )
                .filter(
                    GeoFeature.properties["category"].astext == AppConstants.CATEGORY_POI,
                    GeoFeature.properties["sub_category"].astext == AppConstants.SUB_CATEGORY_RAILWAY,
                    func.ST_DWithin(
                        GeoFeature.geometry, 
                        user_location_geog, 
                        radius_km * AppConstants.METERS_PER_KM
                    )
                )
                .order_by(func.ST_Distance(GeoFeature.geometry, user_location_geog))
                .all()
            )
            
            self.logger.debug(f"Railway search found {len(railways)} results")
            return railways
            
        except Exception as e:
            self.logger.error(f"Error in railway search: {str(e)}")
            raise
    
    def search_by_bbox(
        self, 
        min_lat: float, 
        min_lon: float, 
        max_lat: float, 
        max_lon: float
    ) -> List[GeoFeature]:
        """
        Search features within bounding box
        """
        try:
            bbox = func.ST_MakeEnvelope(
                min_lon, min_lat, max_lon, max_lat, 
                AppConstants.SRID_WGS84
            )
            
            results = (
                self.db.query(GeoFeature)
                .filter(func.ST_Intersects(GeoFeature.geometry, bbox))
                .all()
            )
            
            self.logger.debug(f"BBox search found {len(results)} results")
            return results
            
        except Exception as e:
            self.logger.error(f"Error in bbox search: {str(e)}")
            raise
    
    def search_by_buffer(
        self, 
        lat: float, 
        lon: float, 
        buffer_km: float
    ) -> List[GeoFeature]:
        """
        Search features within buffer zone
        """
        try:
            point = func.ST_SetSRID(
                func.ST_MakePoint(lon, lat), 
                AppConstants.SRID_WGS84
            )
            buffer_geom = func.ST_Buffer(
                point.cast(Geography), 
                buffer_km * AppConstants.METERS_PER_KM
            )
            
            results = (
                self.db.query(GeoFeature)
                .filter(func.ST_Intersects(GeoFeature.geometry, buffer_geom))
                .all()
            )
            
            self.logger.debug(f"Buffer search found {len(results)} results")
            return results
            
        except Exception as e:
            self.logger.error(f"Error in buffer search: {str(e)}")
            raise
    
    def get_autocomplete_suggestions(self, query: str, limit: int = None) -> List[str]:
        """
        Get autocomplete suggestions for search query
        """
        if limit is None:
            limit = settings.DEFAULT_SEARCH_LIMIT
            
        try:
            sim_name = func.similarity(GeoFeature.properties["name"].astext, query)
            sim_project = func.word_similarity(GeoFeature.properties["project"].astext, query)
            
            results = (
                self.db.query(
                    GeoFeature.properties["name"].astext.label("name"),
                    GeoFeature.properties["project"].astext.label("project"),
                    func.greatest(sim_name, sim_project).label("score")
                )
                .filter(
                    func.lower(GeoFeature.properties["name"].astext).ilike(f"%{query.lower()}%") |
                    func.lower(GeoFeature.properties["project"].astext).ilike(f"%{query.lower()}%")
                )
                .order_by(func.greatest(sim_name, sim_project).desc())
                .limit(limit)
                .all()
            )
            
            suggestions = [r.name for r in results if r.name is not None]
            self.logger.debug(f"Autocomplete found {len(suggestions)} suggestions")
            return suggestions
            
        except Exception as e:
            self.logger.error(f"Error in autocomplete: {str(e)}")
            raise
