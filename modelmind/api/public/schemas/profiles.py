from typing import Optional

from pydantic import BaseModel

from .base import BaseResponse


class Profile(BaseModel):
    id: str
    sessions: Optional[list[str]] = None


class ProfileSessionResponse(BaseResponse):
    session_token: str
    session_id: str
    profile_id: str
