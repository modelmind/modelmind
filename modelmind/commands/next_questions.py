from pydantic import BaseModel
from .base import Command
from modelmind.models.questionnaires.base import Questionnaire
from modelmind.models.results.base import Result


class NextQuestions(BaseModel):
    questions: list
    count: int
    completed: bool


class NextQuestionsCommand(Command[NextQuestions]):

    # This command is responsible for fetching the next questions from the database
    # and returning them to the user
    def __init__(self, questionnaire: Questionnaire, current_result: Result) -> None:
        self.questionnaire = questionnaire
        self.current_result = current_result

    async def _run(self) -> NextQuestions:

        questions = await self.questionnaire.infer_next_questions(self.current_result)

        return NextQuestions(
            questions=questions,
            count=len(questions),
            completed=False
        )
