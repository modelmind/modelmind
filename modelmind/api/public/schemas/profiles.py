from typing import Literal, Optional

from pydantic import BaseModel

from .base import BaseResponse


class Profile(BaseModel):
    id: str
    sessions: Optional[list[str]] = None


class SessionResponse(BaseResponse):
    session_id: str
    profile_id: str
    questionnaire_id: str
    language: str
    status: Literal["in_progress", "completed", "expired"]
