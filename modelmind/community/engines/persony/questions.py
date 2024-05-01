from modelmind.models.questions import Question, ScaleQuestion

from .dimensions import PersonyDimension


class PersonyQuestion(Question):
    category: PersonyDimension
    question: ScaleQuestion
