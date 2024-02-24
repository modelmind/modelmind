from enum import StrEnum
from typing import Optional
from uuid import uuid4

from pydantic import Field

from . import DBIdentifierUUID, DBObject, DBObjectCreate, DBOBjectUpdate


class SessionStatus(StrEnum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    EXPIRED = "expired"


class DBCreateSession(DBObjectCreate):
    id: DBIdentifierUUID = Field(default_factory=uuid4)

    profile_id: DBIdentifierUUID
    questionnaire_id: DBIdentifierUUID

    status: SessionStatus
    language: str

    metadata: Optional[dict] = None


class DBSession(DBObject):
    id: DBIdentifierUUID

    profile_id: DBIdentifierUUID
    questionnaire_id: DBIdentifierUUID

    status: SessionStatus
    language: str

    metadata: Optional[dict] = None


class DBUpdateSession(DBOBjectUpdate):
    id: DBIdentifierUUID
    status: Optional[SessionStatus]
