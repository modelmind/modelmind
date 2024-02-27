from . import DBObject, DBObjectCreate


class DBQuestionnaire(DBObject):
    name: str
    engine: str

    config: dict


class CreateQuestionnaire(DBObjectCreate):
    name: str
    engine: str

    config: dict

    questions: list[dict]
