from abc import ABC, abstractmethod
from modelmind.models.engines.base import BaseEngine
from modelmind.models.questions.base import BaseQuestion
from modelmind.models.results.base import BaseResult


class BaseQuestionnaire(ABC):

    name: str

    def __init__(self, engine: BaseEngine, questions: list[BaseQuestion]) -> None:
        self.engine = engine
        self.questions = questions

    @abstractmethod
    async def infer_next_questions(
        self,
        results: BaseResult,
    ) -> list[BaseQuestion]:
        raise NotImplementedError

    @abstractmethod
    async def is_questionnaire_completed(
        self,
        results: BaseResult,
    ) -> bool:
        raise NotImplementedError
