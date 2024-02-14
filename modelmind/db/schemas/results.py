from typing import Optional
from .firestore import Document, DocumentCreate
from uuid import UUID


class CreateResult(DocumentCreate):
    questionnaire_id: UUID
    session_id: UUID

    data: dict

    fingerprint: Optional[str] = None


class ResultDocument(Document):
    questionnaire_id: UUID
    session_id: UUID

    data: dict


class UpdateResultFingerprint(Document):
    fingerprint: str | None = None
