from pydantic import ConfigDict

from . import DBIdentifier, DBObject


class DBQuestion(DBObject):
    questionnaire_id: DBIdentifier
    language: str

    text: str

    model_config = ConfigDict(extra="allow")
