from pydantic import Field
from shortuuid import uuid

from . import DBIdentifier, DBObject, DBObjectCreate


class DBQuestionnaire(DBObject):
    name: str
    engine: str

    config: dict


class CreateQuestionnaire(DBObjectCreate):
    id: DBIdentifier = Field(default_factory=lambda: str(uuid()[:8]))

    name: str
    engine: str

    config: dict

    questions: list[dict]
