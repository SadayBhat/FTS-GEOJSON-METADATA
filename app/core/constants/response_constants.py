class ResponseConstants:
    """API response constants"""
    
    # Success Messages
    SUCCESS = "Success"
    SEARCH_COMPLETED = "Search completed successfully"
    DATA_RETRIEVED = "Data retrieved successfully"
    
    # HTTP Status Codes
    STATUS_OK = 200
    STATUS_CREATED = 201
    STATUS_BAD_REQUEST = 400
    STATUS_NOT_FOUND = 404
    STATUS_INTERNAL_ERROR = 500
    
    # Response Types
    TYPE_FEATURE = "Feature"
    TYPE_FEATURE_COLLECTION = "FeatureCollection"
    
    # Content Types
    CONTENT_TYPE_JSON = "application/json"
    CONTENT_TYPE_GEOJSON = "application/geo+json"
    
    # Error Messages
    NOT_FOUND_MESSAGE = "No features found"
    RAILWAY_NOT_FOUND = "No railway stations found within specified radius"
    BBOX_NOT_FOUND = "No features found in bounding box"
    BUFFER_NOT_FOUND = "No features found in buffer zone"
    
    # Pagination
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100
