from .health import router as health_router
from .profiles.endpoints import router as profile_router
from .questionnaires.endpoints import router as questionnaire_router
from .results.endpoints import router as results_router

__all__ = ["health_router", "profile_router", "questionnaire_router", "results_router"]
