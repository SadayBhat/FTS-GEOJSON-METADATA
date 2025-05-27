from sqlalchemy import Column, Integer, String, JSON, Index, text
from sqlalchemy.dialects.postgresql import JSONB, TSVECTOR
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry

Base = declarative_base()

class GeoFeature(Base):
    """GeoFeature database model"""
    __tablename__ = 'geo_features'

    id = Column(Integer, primary_key=True, index=True)
    feature_type = Column(String)
    properties = Column(JSONB)
    geometry = Column(Geometry(geometry_type='GEOMETRY', srid=4326))
    geom_type = Column(String) 
    coordinates = Column(JSONB)
    search_vector = Column(TSVECTOR)

# Geometry spatial index (gist)
Index(
    "idx_geo_geom",
    GeoFeature.geometry,
    postgresql_using='gist'
)

# GIN index on full-text search vector
Index(
    "idx_geo_features_search_vector",
    GeoFeature.search_vector,
    postgresql_using='gin'
)

# Trigram index on name
Index(
    "idx_name_trgm",
    text("(properties ->> 'name')"),
    postgresql_using='gin',
    postgresql_ops={'(properties ->> \'name\')': 'gin_trgm_ops'}
)

# FTS on name
Index(
    "idx_name_fts",
    text("to_tsvector('english', properties ->> 'name')"),
    postgresql_using='gin'
)

# FTS on project
Index(
    "idx_geo_features_project_fts",
    text("to_tsvector('english', properties ->> 'project')"),
    postgresql_using='gin'
)

# Trigram index on project
Index(
    "idx_project_trgm",
    text("(properties ->> 'project')"),
    postgresql_using='gin',
    postgresql_ops={'(properties ->> \'project\')': 'gin_trgm_ops'}
)
