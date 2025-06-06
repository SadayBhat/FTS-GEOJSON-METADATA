import time
import sys
import os
from fastapi import Request
from loguru import logger
from app.core.constants.logger_constants import LoggerConstants
from app.core.config import settings

os.makedirs(LoggerConstants.LOG_DIR, exist_ok=True)

# Remove default handler
logger.remove()

# Console logger
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level=settings.LOG_LEVEL,
    backtrace=True,
    diagnose=True,
)

# File logger for all logs
logger.add(
    LoggerConstants.APP_LOG_FILE,
    rotation=LoggerConstants.ROTATION_SIZE,
    retention=LoggerConstants.RETENTION_TIME,
    compression=LoggerConstants.COMPRESSION,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="DEBUG",
    backtrace=True,
    diagnose=True,
)

# File logger for error logs
logger.add(
    LoggerConstants.ERROR_LOG_FILE,
    rotation=LoggerConstants.ROTATION_SIZE,
    retention=LoggerConstants.RETENTION_TIME,
    compression=LoggerConstants.COMPRESSION,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="ERROR",
    backtrace=True,
    diagnose=True,
)

async def log_request(request: Request, call_next):
    start_time = time.time()
    logger.info(LoggerConstants.REQUEST_LOG.format(request=f"{request.method} {request.url}"))

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    logger.info(LoggerConstants.RESPONSE_LOG.format(response=f"Status: {response.status_code}"))
    logger.info(LoggerConstants.PROCESS_TIME_LOG.format(time=round(process_time, 2)))

    return response

def get_logger():
    return logger
