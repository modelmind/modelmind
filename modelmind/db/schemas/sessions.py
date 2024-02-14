from enum import StrEnum
from typing import Optional

from .firestore import Document, DocumentCreate, DocumentUpdate


class SessionStatus(StrEnum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    EXPIRED = "expired"


class CreateSession(DocumentCreate):

    questionnaire_id: str

    status: SessionStatus
    language: str

    metadata: Optional[dict] = None


class SessionDocument(Document):

    questionnaire_id: str

    status: SessionStatus
    language: str

    metadata: Optional[dict] = None


class UpdateSession(DocumentUpdate):

    status: Optional[SessionStatus]
