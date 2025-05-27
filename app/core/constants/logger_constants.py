class LoggerConstants:
    """Logging configuration constants"""
    
    # Log Levels
    LEVEL_DEBUG = "DEBUG"
    LEVEL_INFO = "INFO"
    LEVEL_WARNING = "WARNING"
    LEVEL_ERROR = "ERROR"
    LEVEL_CRITICAL = "CRITICAL"
    
    # Log Formats
    DEFAULT_FORMAT = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )
    
    SIMPLE_FORMAT = "{time} | {level} | {message}"
    
    # Log Files
    LOG_DIR = "logs"
    APP_LOG_FILE = "logs/app.log"
    ERROR_LOG_FILE = "logs/error.log"
    ACCESS_LOG_FILE = "logs/access.log"
    
    # Rotation Settings
    ROTATION_SIZE = "10 MB"
    RETENTION_TIME = "30 days"
    COMPRESSION = "zip"
    
    # Logger Names
    LOGGER_APP = "fts_app"
    LOGGER_DATABASE = "fts_database"
    LOGGER_API = "fts_api"
    LOGGER_SERVICE = "fts_service"

    DB_CONNECT_ERROR = "Database connection error: {error}"
    DB_CONNECT_RETRY_FAIL = "Failed to connect to the database after {retries} attempts."
    DB_CONNECT_SUCCESS = "Successfully connected to the database"

    APP_STARTUP = "Application startup initiated."
    APP_SHUTDOWN = "Application shutdown completed."
    REQUEST_LOG = "Request: {request}"

    DB_CONNECT_ERROR = "Database connection error: {error}"
    DB_SESSION_ERROR = "Database session error: {error}"
    DB_CONNECT_RETRY_FAIL = "Failed to connect to the database after {retries} attempts."

    # Database logging
    DB_CONNECT_SUCCESS = "Successfully connected to the database"
    DB_CONNECT_ERROR = "Failed to connect to the database: {error}"

    # Error logging
    ERROR_LOG = "Error: {error}"
    HTTP_ERROR_LOG = "HTTP Error: {error}"

    # Request/response logging
    REQUEST_LOG = "Request: {request}"
    RESPONSE_LOG = "Response: {response}"
    PROCESS_TIME_LOG = "Process time: {time}ms"