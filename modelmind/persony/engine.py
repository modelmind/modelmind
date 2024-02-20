from modelmind.models.questions.base import BaseQuestion
from modelmind.models.questionnaires.base import BaseQuestionnaire
from modelmind.models.results.base import BaseResult
from modelmind.models.engines.base import BaseEngine
from modelmind.persony.dimensions import PersonyDimension
from modelmind.persony.question import PersonyQuestion


class PersonyEngineV1(BaseEngine):

    def __init__(self, questions: list[PersonyQuestion], results: list[BaseResult]) -> None:
        self.questions = questions
        self.current_step = 0

    async def infer_next_questions(self, results: BaseResult) -> list[BaseQuestion]:
        return []




