from sqlalchemy import Column, Integer, String, JSON, Index, text
from sqlalchemy.dialects.postgresql import JSONB, TSVECTOR
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry
from app.core.constants.app_constants import AppConstants

Base = declarative_base()

class GeoFeature(Base):
    __tablename__ = AppConstants.TABLE_NAME

    id = Column(Integer, primary_key=True, index=True)
    properties = Column(JSONB)

    search_vector = Column(TSVECTOR)

# GIN index on full-text search vector
Index(
    AppConstants.SEARCH_VECTOR_INDEX_GIN,
    GeoFeature.search_vector,
    postgresql_using='gin'
)

# Trigram index on name
Index(
    AppConstants.TRIGRAM_INDEX_NAME_GIN,
    text("(properties ->> 'name')"),
    postgresql_using='gin',
    postgresql_ops={'(properties ->> \'name\')': 'gin_trgm_ops'}
)

# FTS on name
Index(
    AppConstants.NAME_INDEX_GIN,
    text("to_tsvector('english', properties ->> 'name')"),
    postgresql_using='gin'
)

# FTS on project
Index(
    AppConstants.PROJECT_INDEX_GIN,
    text("to_tsvector('english', properties ->> 'project')"),
    postgresql_using='gin'
)

# Trigram index on project
Index(
    AppConstants.PROJECT_TRIGRAM_INDEX_GIN,
    text("(properties ->> 'project')"),
    postgresql_using='gin',
    postgresql_ops={'(properties ->> \'project\')': 'gin_trgm_ops'}
)

# FTS on STD_CODE 
Index(
    AppConstants.STD_CODE_INDEX_GIN,
    text("(properties ->> 'std_code')"),
    postgresql_using='gin'
)


