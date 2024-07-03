from fastapi import APIRouter

from .endpoints.profile import router as profile_router
from .endpoints.questionnaire import router as questionnaire_router
from .endpoints.results import router as results_router
from .endpoints.health import router as health_router

public_v1_router = APIRouter(prefix="/v1/public", tags=["Public"])
public_v1_router.include_router(router=profile_router)
public_v1_router.include_router(router=questionnaire_router)
public_v1_router.include_router(router=results_router)
public_v1_router.include_router(router=health_router)


__all__ = ["public_v1_router"]
