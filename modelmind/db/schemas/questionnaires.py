from typing import Optional, TypedDict

from . import DBObject


class QuestionnaireConfig(TypedDict, total=False):
    engine: dict


class DBQuestionnaire(DBObject):
    name: str
    description: Optional[str]
    engine: str

    config: QuestionnaireConfig = QuestionnaireConfig()

    owner: str
    visibility: str
