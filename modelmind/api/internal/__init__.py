from fastapi import APIRouter

from modelmind.api.internal.endpoints.statistics import router as statistics_router

internal_v1_router = APIRouter(prefix="/v1/internal", tags=["Internal"])
internal_v1_router.include_router(router=statistics_router)

__all__ = ["internal_v1_router"]
