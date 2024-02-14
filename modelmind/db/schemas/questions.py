from .firestore import Document
from uuid import UUID
from pydantic import ConfigDict


class QuestionDocument(Document):
    questionnaire_id: UUID
    language: str

    text: str

    model_config = ConfigDict(extra="allow")
