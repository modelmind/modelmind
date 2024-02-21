from modelmind.models.questions import Question
from modelmind.models.questionnaires import Questionnaire
from modelmind.models.results import Result
from modelmind.models.engines.base import BaseEngine


class PersonyEngineV1(BaseEngine):

    def __init__(self, questions: list[Question]) -> None:
        self.questions = questions
        self.current_step = 0

    async def infer_next_questions(self, current_result: Result) -> list[Question]:
        return []

