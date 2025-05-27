import os
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database.rds import Base, engine
from app.api.v1.endpoints.routes import router as api_router
from app.core.logger.logging import log_request, get_logger
from app.core.config import settings
from app.core.constants.logger_constants import LoggerConstants

# Get logger
logger = get_logger()

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info(LoggerConstants.APP_STARTUP)
        Base.metadata.create_all(bind=engine)
        with engine.connect() as conn:
            logger.info(LoggerConstants.DB_CONNECT_SUCCESS)
    except Exception as e:
        logger.error(LoggerConstants.DB_CONNECT_ERROR.format(error=str(e)))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=LoggerConstants.DB_CONNECT_ERROR.format(error=str(e))
        )
    yield
    logger.info(LoggerConstants.APP_SHUTDOWN)

# Initialize FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A FastAPI application for full-text search of documents",
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    lifespan=lifespan
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging middleware
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    return await log_request(request, call_next)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_PREFIX, tags=["FTS-Document-Search"])
