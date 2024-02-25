from typing import Optional

from . import DBIdentifier, DBObject, DBObjectCreate, DBOBjectUpdate


class DBResult(DBObject):
    questionnaire_id: DBIdentifier
    session_id: DBIdentifier

    data: dict


class CreateResult(DBObjectCreate):
    questionnaire_id: DBIdentifier
    session_id: DBIdentifier

    data: dict

    user_hash: Optional[str] = None


class UpdateResultPublicKey(DBOBjectUpdate):
    user_hash: str | None = None
