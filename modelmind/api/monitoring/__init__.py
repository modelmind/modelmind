from fastapi import APIRouter

from .health import router as health_router

monitoring_router = APIRouter(prefix="/monitoring", tags=["Monitoring"])
monitoring_router.include_router(health_router)

__all__ = ["monitoring_router"]
