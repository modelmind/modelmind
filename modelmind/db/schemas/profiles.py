from typing import List


from . import DBIdentifier, DBObject, DBObjectCreate


class CreateProfile(DBObjectCreate):
    ...


class DBProfile(DBObject):
    id: DBIdentifier
    sessions: List[DBIdentifier] = []
    results: List[DBIdentifier] = []
