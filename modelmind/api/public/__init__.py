from fastapi import APIRouter

public_v1_router = APIRouter(prefix="/v1/public", tags=["Public"])


__all__ = ["public_v1_router"]
