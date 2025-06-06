from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, desc
from loguru import logger
from fastapi import HTTPException, status
from app.database.models import GeoFeature
from app.core.constants.app_constants import AppConstants
from app.core.config import settings
from app.core.constants.logger_constants import LoggerConstants
from app.core.constants.exception_constants import ExceptionConstants


class GeoFeatureDAO:

    def __init__(self, db: Session):
        self.db = db
        self.logger = logger.bind(name="GeoFeatureDAO")

    def clean_properties(self, geo_feature: GeoFeature) -> dict:
        return {k: v for k, v in geo_feature.properties.items() if v is not None}

    # Full-Text-Search
    def search_by_text(self, query: str, limit: int = settings.DEFAULT_SEARCH_LIMIT) -> List[GeoFeature]:
        try:
            ts_query = func.plainto_tsquery(AppConstants.VECTOR_LANGUAGE, query)
            results = (
                self.db.query(GeoFeature)
                .filter(GeoFeature.search_vector.op("@@")(ts_query))
                .limit(limit)
                .all()
            )

            cleaned_results = [
                GeoFeature(properties=self.clean_properties(geo_feature))
                for geo_feature in results
            ]

            self.logger.debug(LoggerConstants.FULLTEXT_SEARCH_SUCCESS.format(count=len(cleaned_results)))
            return cleaned_results

        except Exception as e:
            self.logger.error(LoggerConstants.FULLTEXT_SEARCH_ERROR.format(error=str(e)))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=ExceptionConstants.FULLTEXT_SEARCH_ERROR.format(error=str(e))
            )

    # Fuzzy Search
    def search_by_similarity(self, query: str, limit: int = settings.DEFAULT_SEARCH_LIMIT) -> List[GeoFeature]:
        try:
            similarity_threshold = 0.15
            query_lower = query.lower()

            sim_name = func.word_similarity(GeoFeature.properties["name"].astext, query)
            sim_project = func.word_similarity(GeoFeature.properties["project"].astext, query)
            sim_cat = func.word_similarity(GeoFeature.properties["category"].astext, query)
            sim_subcat = func.word_similarity(GeoFeature.properties["sub_category"].astext, query)
            sim_lane = func.word_similarity(GeoFeature.properties["lane"].astext, query)
            sim_landarea = func.word_similarity(GeoFeature.properties["land_area"].astext, query)

            results = (
                self.db.query(GeoFeature)
                .filter(
                    or_(
                        GeoFeature.properties["name"].astext.ilike(f"%{query_lower}%"),
                        GeoFeature.properties["project"].astext.ilike(f"%{query_lower}%"),
                        GeoFeature.properties["category"].astext.ilike(f"%{query_lower}%"),
                        GeoFeature.properties["sub_category"].astext.ilike(f"%{query_lower}%"),
                        GeoFeature.properties["lane"].astext.ilike(f"%{query_lower}%"),
                        GeoFeature.properties["land_area"].astext.ilike(f"%{query_lower}%"),
                        sim_name >= similarity_threshold,
                        sim_project >= similarity_threshold,
                        sim_cat >= similarity_threshold,
                        sim_subcat >= similarity_threshold,
                        sim_lane >= similarity_threshold,
                        sim_landarea >= similarity_threshold
                    )
                )
                .order_by(
                    desc(
                        sim_name * 1.4 +
                        sim_project * 1.2 +
                        sim_cat * 1.0 +
                        sim_subcat * 0.8 +
                        sim_landarea * 0.6 +
                        sim_lane * 0.4
                    )
                )
                .limit(limit)
                .all()
            )

            cleaned_results = [
                GeoFeature(properties=self.clean_properties(geo_feature))
                for geo_feature in results
            ]

            self.logger.debug(LoggerConstants.SIMILARITY_SEARCH_SUCCESS.format(count=len(cleaned_results)))
            return cleaned_results

        except Exception as e:
            self.logger.error(LoggerConstants.SIMILARITY_SEARCH_ERROR.format(error=str(e)))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=ExceptionConstants.SIMILARITY_SEARCH_ERROR.format(error=str(e))
            )

    # Autocomplete 
    def get_autocomplete_suggestions(self, query: str, limit: int = None) -> List[str]:
        if limit is None:
            limit = settings.DEFAULT_SEARCH_LIMIT

        try:
            query_lower = query.lower()

            sim_name = func.similarity(GeoFeature.properties["name"].astext, query)
            sim_project = func.similarity(GeoFeature.properties["project"].astext, query)
            sim_cat = func.similarity(GeoFeature.properties["category"].astext, query)
            sim_subcat = func.similarity(GeoFeature.properties["sub_category"].astext, query)
            sim_lane = func.similarity(GeoFeature.properties["lane"].astext, query)

            results = (
                self.db.query(
                    GeoFeature.properties["name"].astext.label("name"),
                    GeoFeature.properties["project"].astext.label("project"),
                    GeoFeature.properties["category"].astext.label("category"),
                    GeoFeature.properties["sub_category"].astext.label("sub_category"),
                    GeoFeature.properties["lane"].astext.label("lane"),
                    func.greatest(sim_name, sim_project, sim_cat, sim_subcat, sim_lane).label("score")
                )
                .filter(
                    or_(
                        GeoFeature.properties["name"].astext.ilike(f"%{query_lower}%"),
                        GeoFeature.properties["project"].astext.ilike(f"%{query_lower}%"),
                        GeoFeature.properties["category"].astext.ilike(f"%{query_lower}%"),
                        GeoFeature.properties["sub_category"].astext.ilike(f"%{query_lower}%"),
                        GeoFeature.properties["lane"].astext.ilike(f"%{query_lower}%")
                    )
                )
                .order_by(desc("score"))
                .limit(limit)
                .all()
            )

            suggestions = [
                f"{r.name} - {r.project or r.sub_category or r.category}" if r.name else ""
                for r in results if r.name
            ]

            self.logger.debug(LoggerConstants.AUTOCOMPLETE_SUCCESS.format(count=len(suggestions)))
            return suggestions

        except Exception as e:
            self.logger.error(LoggerConstants.AUTOCOMPLETE_ERROR.format(error=str(e)))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=ExceptionConstants.AUTOCOMPLETE_ERROR.format(error=str(e))
            )

    def search_by_unified_filter(
        self,
        query: str,
        filter_value: str = None,
        limit: int = settings.DEFAULT_SEARCH_LIMIT
    ) -> List[GeoFeature]:
        try:
            base_query = self.db.query(GeoFeature)

            # Apply the unified filter if provided
            if filter_value:
                base_query = base_query.filter(
                    or_(
                        GeoFeature.properties["category"].astext.ilike(f"%{filter_value}%"),
                        GeoFeature.properties["sub_category"].astext.ilike(f"%{filter_value}%"),
                        GeoFeature.properties["name"].astext.ilike(f"%{filter_value}%")  # if applicable
                    )
                )

            ts_query = func.plainto_tsquery(AppConstants.VECTOR_LANGUAGE, query)
            results = (
                base_query
                .filter(GeoFeature.search_vector.op("@@")(ts_query))
                .limit(limit)
                .all()
            )

            cleaned_results = [
                GeoFeature(properties=self.clean_properties(geo_feature))
                for geo_feature in results
            ]

            self.logger.debug(LoggerConstants.FULLTEXT_SEARCH_SUCCESS.format(count=len(cleaned_results)))
            return cleaned_results

        except Exception as e:
            self.logger.error(LoggerConstants.FULLTEXT_SEARCH_ERROR.format(error=str(e)))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=ExceptionConstants.FULLTEXT_SEARCH_ERROR.format(error=str(e))
            )




    # def search_by_filters(
    #     self,
    #     query: str,
    #     category: str = None,
    #     sub_category: str = None,
    #     limit: int = settings.DEFAULT_SEARCH_LIMIT
    #     ) -> List[GeoFeature]:

    #     try:
    #         # Start with base query
    #         base_query = self.db.query(GeoFeature)

    #         # Apply category/sub_category filters if provided
    #         if category:
    #             base_query = base_query.filter(
    #                 GeoFeature.properties["category"].astext.ilike(f"%{category}%")
    #             )
    #         if sub_category:
    #             base_query = base_query.filter(
    #                 GeoFeature.properties["sub_category"].astext.ilike(f"%{sub_category}%")
    #             )

    #         # Run FTS on the filtered results
    #         ts_query = func.plainto_tsquery(AppConstants.VECTOR_LANGUAGE, query)
    #         results = (
    #             base_query
    #             .filter(GeoFeature.search_vector.op("@@")(ts_query))
    #             .limit(limit)
    #             .all()
    #         )

    #         cleaned_results = [
    #             GeoFeature(properties=self.clean_properties(geo_feature))
    #             for geo_feature in results
    #         ]

    #         self.logger.debug(LoggerConstants.FULLTEXT_SEARCH_SUCCESS.format(count=len(cleaned_results)))
    #         return cleaned_results

    #     except Exception as e:
    #         self.logger.error(LoggerConstants.FULLTEXT_SEARCH_ERROR.format(error=str(e)))
    #         raise HTTPException(
    #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             detail=ExceptionConstants.FULLTEXT_SEARCH_ERROR.format(error=str(e))
    #         )

    def upsert_feature(self, properties: dict):
        try:
            geohash_id = properties.get("geohash_id")
            result = (
                self.db.query(GeoFeature)
                .filter(GeoFeature.properties["geohash_id"].astext == geohash_id)
                .first()
            )

            if result:
                result.properties = properties
            else:
                new_feature = GeoFeature(properties=properties)
                self.db.add(new_feature)

            self.db.commit()

        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Error upserting feature: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=ExceptionConstants.GEOJSON_DB_UPSERT_ERROR
            )