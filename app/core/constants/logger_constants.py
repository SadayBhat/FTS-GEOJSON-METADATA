class LoggerConstants:
        
    LOG_DIR = "logs"
    APP_LOG_FILE = "logs/app.log"
    ERROR_LOG_FILE = "logs/error.log"
    
    ROTATION_SIZE = "10 MB"
    RETENTION_TIME = "30 days"
    COMPRESSION = "zip"

    DB_CONNECT_ERROR = "Database connection error: {error}"
    DB_CONNECT_RETRY_FAIL = "Failed to connect to the database after {retries} attempts."
    DB_CONNECT_SUCCESS = "Successfully connected to the database"

    APP_STARTUP = "Application startup initiated."
    APP_SHUTDOWN = "Application shutdown completed."
    REQUEST_LOG = "Request: {request}"

    DB_CONNECT_ERROR = "Database connection error: {error}"
    DB_SESSION_ERROR = "Database session error: {error}"
    DB_CONNECT_RETRY_FAIL = "Failed to connect to the database after {retries} attempts."

    DB_CONNECT_SUCCESS = "Successfully connected to the database"
    DB_CONNECT_ERROR = "Failed to connect to the database: {error}"

    REQUEST_LOG = "Request: {request}"
    RESPONSE_LOG = "Response: {response}"
    PROCESS_TIME_LOG = "Process time: {time}ms"

    SEARCH_ERROR = "Error during search operation"

    FULLTEXT_SEARCH_SUCCESS = "Full-text search found {count} results"
    FULLTEXT_SEARCH_ERROR = "Error in full-text search: {error}"

    SIMILARITY_SEARCH_SUCCESS = "Similarity search found {count} results"
    SIMILARITY_SEARCH_ERROR = "Error in similarity search: {error}"

    AUTOCOMPLETE_SUCCESS = "Autocomplete found {count} suggestions"
    AUTOCOMPLETE_ERROR = "Error in autocomplete: {error}"
