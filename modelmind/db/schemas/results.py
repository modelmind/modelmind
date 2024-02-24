from typing import Optional

from . import DBIdentifierUUID, DBObject, DBObjectCreate, DBOBjectUpdate


class DBResult(DBObject):
    questionnaire_id: DBIdentifierUUID
    session_id: DBIdentifierUUID

    data: dict


class CreateResult(DBObjectCreate):
    questionnaire_id: DBIdentifierUUID
    session_id: DBIdentifierUUID

    data: dict

    user_hash: Optional[str] = None


class UpdateResultPublicKey(DBOBjectUpdate):
    user_hash: str | None = None
