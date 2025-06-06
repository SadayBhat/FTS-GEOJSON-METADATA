class AppConstants:
    
    CATEGORY_POI = "POI"
    SUB_CATEGORY_RAILWAY = "Railway Stations"
    
    SRID = 4326
    GEOMETRY_TYPE = "GEOMETRY"
    
    METERS_PER_KM = 1000
    
    RETRY_ATTEMPTS = 3
    DELAY_TIME = 5

    TABLE_NAME = "geo_features1"

    GEOMETRY_INDEX_GIN = "idx_geo_geom"
    SEARCH_VECTOR_INDEX_GIN = "idx_geo_features_search_vector"
    TRIGRAM_INDEX_NAME_GIN = "idx_name_trgm"
    NAME_INDEX_GIN = "idx_name_fts"
    PROJECT_INDEX_GIN = "idx_geo_features_project_fts"
    PROJECT_TRIGRAM_INDEX_GIN = "idx_project_trgm"
    STD_CODE_INDEX_GIN = "idx_std_code"

    VECTOR_LANGUAGE="english"