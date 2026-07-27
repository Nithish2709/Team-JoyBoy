from fastapi import APIRouter
from app.api.v1.endpoints import health

api_router = APIRouter()

# Mount health routes under /health prefix
api_router.include_router(health.router, prefix="/health", tags=["Health Checks"])
