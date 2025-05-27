class AppConstants:
    """Application-wide constants"""
    
    # Feature Types
    FEATURE_TYPE_POI = "POI"
    FEATURE_TYPE_GEOMETRY = "Feature"
    
    # Categories
    CATEGORY_POI = "POI"
    SUB_CATEGORY_RAILWAY = "Railway Stations"
    
    # Coordinate System
    SRID_WGS84 = 4326
    
    # Units
    METERS_PER_KM = 1000
    
    # Search
    MIN_QUERY_LENGTH = 1
    MAX_SEARCH_RESULTS = 100
    
    # Geometry Types
    GEOM_TYPE_POINT = "Point"
    GEOM_TYPE_LINESTRING = "LineString"
    GEOM_TYPE_POLYGON = "Polygon"
    GEOM_TYPE_MULTIPOINT = "MultiPoint"
    GEOM_TYPE_MULTILINESTRING = "MultiLineString"
    GEOM_TYPE_MULTIPOLYGON = "MultiPolygon"

    RETRY_ATTEMPTS=3
    DELAY_TIME=5
