from typing import Optional

from modelmind.api.business.schemas import BaseResponse
from modelmind.models.questions.schemas import Question

# TODO: we may want to decouple the response schema from the domain model
# Use a response builder/factory?


class NextQuestionsResponse(BaseResponse):
    questions: list[Question]
    completed: int
    remaining: int
    result_id: Optional[str] = None


class SessionLanguageUpdateRequest(BaseResponse):
    language: str
