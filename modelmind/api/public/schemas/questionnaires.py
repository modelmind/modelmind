from modelmind.models.questions.base import Question

from .base import BaseResponse

# TODO: we may want to decouple the response schema from the domain model
# Use a response builder/factory?


class NextQuestionsResponse(BaseResponse):
    questions: list[Question]
    completed: bool
