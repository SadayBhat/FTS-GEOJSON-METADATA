class ExceptionConstants:
    
    SEARCH_ERROR = "Error during search operation"
    DB_CONNECTION_FAILED = "Database connection failed after {retries} attempts: {error}"
    DB_SESSION_FAILED="Database session failed"

    FULLTEXT_SEARCH_ERROR = "Error in full-text search: {error}"
    SIMILARITY_SEARCH_ERROR = "Error in similarity search: {error}"    
    AUTOCOMPLETE_ERROR = "Error in autocomplete: {error}"

    INVALID_FILE_TYPE = "Only .geojson or .json files are accepted."
    INVALID_GEOJSON_FORMAT = "Uploaded file is not a valid GeoJSON."
    MISSING_FEATURES = "GeoJSON does not contain 'features'."
    GEOJSON_DB_UPSERT_ERROR = "Failed to upsert feature to database."
