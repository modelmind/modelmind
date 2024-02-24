from uuid import UUID

from pydantic import ConfigDict

from . import DBObject


class DBQuestion(DBObject):
    questionnaire_id: UUID
    language: str

    text: str

    model_config = ConfigDict(extra="allow")
