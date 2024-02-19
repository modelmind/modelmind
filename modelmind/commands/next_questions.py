from pydantic import BaseModel
from .base import Command
from modelmind.models.questionnaires.base import BaseQuestionnaire

class NextQuestionsParameters(BaseModel):
    questionnaire_id: str
    language: str
    results: dict


class NextQuestion(BaseModel):
    id: str
    text: str
    type: str
    options: list


class NextQuestionsCommand(Command[NextQuestionsParameters, list[NextQuestion]]):
    # This command is responsible for fetching the next questions from the database
    # and returning them to the user
    def __init__(self, params):
        super().__init__(params)

    async def _run(self) -> list[NextQuestion]:
        return []
