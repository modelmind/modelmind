from typing import Optional

from modelmind.models.questions.schemas import Question

from .base import BaseResponse

# TODO: we may want to decouple the response schema from the domain model
# Use a response builder/factory?


class NextQuestionsResponse(BaseResponse):
    questions: list[Question]
    completed: int
    remaining: int
    result_id: Optional[str] = None
