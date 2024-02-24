from typing import Optional

from pydantic import BaseModel


class Profile(BaseModel):
    id: str
    sessions: Optional[list[str]] = None
