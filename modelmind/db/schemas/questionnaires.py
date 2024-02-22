from . import DBIdentifierUUID, DBObject


class DBQuestionnaire(DBObject):
    id: DBIdentifierUUID
    name: str
    engine: str

    config: dict
