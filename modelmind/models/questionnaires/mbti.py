from .base import BaseQuestionnaire
from modelmind.models.engines.base import BaseEngine


class MBTIQuestionnaire(BaseQuestionnaire):

    type: str

    questions: list
    engine: BaseEngine
