from typing import Optional

from . import DBObject


class DBQuestionnaire(DBObject):
    name: str
    description: Optional[str]
    engine: str

    config: dict

    owner: str
    visibility: str
