from enum import StrEnum
from typing import Optional

from . import DBIdentifier, DBObject, DBObjectCreate, DBOBjectUpdate


class ResultVisibility(StrEnum):
    PUBLIC = "public"
    PRIVATE = "private"


class DBResult(DBObject):
    questionnaire_id: DBIdentifier
    session_id: DBIdentifier

    data: dict

    visibility: ResultVisibility = ResultVisibility.PRIVATE


class CreateResult(DBObjectCreate):
    questionnaire_id: DBIdentifier
    session_id: DBIdentifier

    data: dict

    user_hash: Optional[str] = None


class UpdateResultPublicKey(DBOBjectUpdate):
    user_hash: str | None = None


class UpdateResultVisibility(DBOBjectUpdate):
    visibility: ResultVisibility
