from enum import StrEnum
from typing import Optional

from . import DBIdentifier, DBObject, DBOBjectUpdate


class SessionStatus(StrEnum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    EXPIRED = "expired"


class DBSession(DBObject):
    profile_id: DBIdentifier
    questionnaire_id: DBIdentifier

    status: SessionStatus
    language: str

    metadata: Optional[dict] = None


class DBUpdateSession(DBOBjectUpdate):
    status: Optional[SessionStatus]
