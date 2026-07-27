from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from app.core.config import settings
from app.core.logging import setup_logging
from app.db.redis import redis_manager
from app.middleware.request_log import RequestLoggingMiddleware
from app.api.v1.router import api_router

# Configure centralized logging immediately on bootstrap
setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Application startup lifecycle
    logger.info("Starting up FastAPI application process...")
    # Initialize Redis connection pool
    redis_manager.init_pool()
    logger.info("Application infrastructure connections active.")
    yield
    # Application shutdown lifecycle
    logger.info("Initiating application process cleanup...")
    # Close Redis connection pool
    await redis_manager.close_pool()
    logger.info("Application context terminated successfully.")

# Initialize FastAPI with versioned docs settings
app = FastAPI(
    title="PDS Sentinel AI - Backend Platform",
    description="Multi-Agent Intelligent Public Distribution Monitoring Platform Backend base.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# CORS validation config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Attach request-response diagnostic log wrapper
app.add_middleware(RequestLoggingMiddleware)

# Catch-all exception callback mapping unhandled runtime faults
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(f"Encountered unhandled application fault at {request.url.path}: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": {
                "error_code": "INTERNAL_SERVER_ERROR",
                "message": "An unhandled error occurred while processing the request.",
                "details": str(exc) if settings.DEBUG else None
            }
        }
    )

# Register v1 router mappings under the designated suffix (e.g. /api/v1)
app.include_router(api_router, prefix=settings.API_PREFIX)

@app.get("/")
async def root_redirect() -> dict:
    """
    Default root routing guide.
    """
    return {
        "message": "Welcome to PDS Sentinel AI Platform API",
        "documentation": "/docs"
    }
