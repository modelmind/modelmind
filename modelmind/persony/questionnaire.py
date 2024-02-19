from ..models.questionnaires.base import BaseQuestionnaire
from modelmind.models.engines.base import BaseEngine


class PersonyQuestionnaire(BaseQuestionnaire):

    type: str

    questions: list
    engine: BaseEngine



    def next(self):
        pass
