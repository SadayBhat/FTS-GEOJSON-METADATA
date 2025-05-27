class ExceptionConstants:
    """Exception message constants"""
    
    # General Errors
    INTERNAL_SERVER_ERROR = "Internal server error"
    DATABASE_CONNECTION_ERROR = "Database connection failed"
    INVALID_REQUEST = "Invalid request parameters"
    
    # Search Errors
    SEARCH_ERROR = "Error during search operation"
    RAILWAY_SEARCH_ERROR = "Error during railway search"
    BBOX_SEARCH_ERROR = "Error during bounding box search"
    BUFFER_SEARCH_ERROR = "Error during buffer zone search"
    AUTOCOMPLETE_ERROR = "Error during autocomplete operation"
    
    # Data Errors
    NO_RESULTS_FOUND = "No results found"
    INVALID_COORDINATES = "Invalid coordinates provided"
    INVALID_GEOMETRY = "Invalid geometry data"
    
    # Validation Errors
    QUERY_TOO_SHORT = "Query string is too short"
    INVALID_RADIUS = "Invalid radius value"
    INVALID_BUFFER = "Invalid buffer value"
    INVALID_BBOX = "Invalid bounding box coordinates"

    DB_CONNECTION_FAILED = "Database connection failed after {retries} attempts: {error}"