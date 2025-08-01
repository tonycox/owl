from fastapi import APIRouter

from .endpoints import health, owl

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(owl.router, prefix="/owl", tags=["owl"])
