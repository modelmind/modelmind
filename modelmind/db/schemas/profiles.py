from typing import List

from . import DBIdentifierUUID, DBObject, DBObjectCreate


class CreateProfile(DBObjectCreate):
    ...


class DBProfile(DBObject):
    id: DBIdentifierUUID
    sessions: List[DBIdentifierUUID]
    results: List[DBIdentifierUUID]
