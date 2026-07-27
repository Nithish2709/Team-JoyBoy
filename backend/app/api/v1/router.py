"""
API v1 router — aggregates all endpoint routers.
"""
from fastapi import APIRouter
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.users import router as users_router
from app.api.v1.endpoints.districts import router as districts_router
from app.api.v1.endpoints.shops import router as shops_router
from app.api.v1.endpoints.warehouses import router as warehouses_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(districts_router)
api_router.include_router(shops_router)
api_router.include_router(warehouses_router)
