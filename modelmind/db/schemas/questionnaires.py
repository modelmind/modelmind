from . import DBObject


class DBQuestionnaire(DBObject):
    name: str
    engine: str

    config: dict
