from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.db.database import get_async_db
from app.db.redis import check_redis_health
from loguru import logger

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("", status_code=status.HTTP_200_OK)
async def get_general_health() -> dict:
    """
    General check verifying the web server is running and responding.
    """
    return {
        "status": "healthy",
        "service": "PDS Sentinel AI Backend",
        "status_code": status.HTTP_200_OK
    }

@router.get("/database", status_code=status.HTTP_200_OK)
async def get_database_health(db: AsyncSession = Depends(get_async_db)) -> dict:
    """
    Performs an active check of the PostgreSQL engine using SELECT 1.
    """
    try:
        result = await db.execute(text("SELECT 1"))
        val = result.scalar()
        if val == 1:
            return {
                "status": "healthy",
                "database": "connected",
                "status_code": status.HTTP_200_OK
            }
        raise ValueError("Invalid return from DB query.")
    except Exception as exc:
        logger.error(f"Database validation check failed: {str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "unhealthy",
                "database": "disconnected",
                "error": str(exc)
            }
        )

@router.get("/redis", status_code=status.HTTP_200_OK)
async def get_redis_health() -> dict:
    """
    Performs an active health check of Redis cache connectivity.
    """
    is_healthy = await check_redis_health()
    if is_healthy:
        return {
            "status": "healthy",
            "redis": "connected",
            "status_code": status.HTTP_200_OK
        }
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail={
            "status": "unhealthy",
            "redis": "disconnected"
        }
    )
