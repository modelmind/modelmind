from modelmind.models.questions import Question

from .dimensions import PersonyDimension


class PersonyQuestion(Question):
    category: PersonyDimension
