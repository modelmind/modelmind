from enum import StrEnum

from . import DBIdentifier, DBObject, DBOBjectUpdate


class ResultVisibility(StrEnum):
    PUBLIC = "public"
    PRIVATE = "private"


class DBResult(DBObject):
    questionnaire_id: DBIdentifier
    session_id: DBIdentifier

    data: dict

    visibility: ResultVisibility = ResultVisibility.PRIVATE
    label: str


class UpdateResultPublicKey(DBOBjectUpdate):
    user_hash: str | None = None


class UpdateResultVisibility(DBOBjectUpdate):
    visibility: ResultVisibility
