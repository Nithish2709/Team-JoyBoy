import logging
import sys
from loguru import logger
from app.core.config import settings

def setup_logging() -> None:
    # Clean default handlers from standard logging library
    logging.root.handlers = []

    log_level = "DEBUG" if settings.DEBUG else "INFO"
    
    # Configure Loguru sinks (Console and Log File)
    config = {
        "handlers": [
            {
                "sink": sys.stdout,
                "level": log_level,
                "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
                "colorize": True,
            },
            {
                "sink": "logs/backend.log",
                "level": log_level,
                "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
                "rotation": "10 MB",
                "retention": "7 days",
                "compression": "zip",
            }
        ]
    }
    
    logger.configure(**config)

    # Logging Interceptor class mapping python's basic logger to loguru handlers
    class InterceptHandler(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = str(record.levelno)

            frame, depth = logging.currentframe(), 2
            while frame and frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

    # Forward specific framework logs to Loguru
    for logger_name in ("uvicorn", "uvicorn.access", "uvicorn.error", "sqlalchemy.engine", "alembic"):
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = [InterceptHandler()]
        logging_logger.propagate = False

    logger.info("Centralized logging initialization completed.")
