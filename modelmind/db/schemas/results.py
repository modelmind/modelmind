from typing import Optional
from . import DBObject, DBObjectCreate, DBOBjectUpdate
from uuid import UUID


class Result(DBObject):
    questionnaire_id: UUID
    session_id: UUID

    data: dict


class CreateResult(DBObjectCreate):
    questionnaire_id: UUID
    session_id: UUID

    data: dict

    fingerprint: Optional[str] = None


class UpdateResultFingerprint(DBOBjectUpdate):
    fingerprint: str | None = None
