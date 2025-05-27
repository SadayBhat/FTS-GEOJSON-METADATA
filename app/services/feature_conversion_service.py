from geoalchemy2.shape import to_shape
from shapely.geometry import mapping
from app.core.models.pydantic_models import FeatureOut, GeometrySchema
from app.core.constants.response_constants import ResponseConstants
from app.database.models import GeoFeature
from loguru import logger


class FeatureConversionService:

    @staticmethod
    def convert(geo_feature: GeoFeature) -> FeatureOut:
        try:
            shapely_geom = to_shape(geo_feature.geometry)
            geometry_dict = mapping(shapely_geom)

            clean_properties = {
                k: v for k, v in geo_feature.properties.items() if v is not None
            }

            return FeatureOut(
                type=ResponseConstants.TYPE_FEATURE,
                properties=clean_properties,
                geometry=GeometrySchema(**geometry_dict),
                distance_Km=None
            )
        except Exception as e:
            logger.error(f"[FeatureConversion] Error: {e}")
            raise
