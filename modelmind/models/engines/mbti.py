from .base import SimpleEngine
from modelmind.models.questions.base import BaseQuestion
from modelmind.models.questionnaires.base import BaseQuestionnaire
from modelmind.models.results.base import BaseResult
from modelmind.models.theories.mbti.trait import MBTITraits
from modelmind.models.theories.jung.functions import JungFunctions


class MBTIAdaptiveEngine(SimpleEngine):

    def __init__(self, questions: list[BaseQuestion]) -> None:
        self.questions = questions

    async def infer_next_questions(self, results: BaseResult) -> list[BaseQuestion]:
        return []
