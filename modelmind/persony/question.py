from modelmind.models.questions.base import BaseQuestion


Dimension = str

class PersonyQuestion(BaseQuestion):

    @property
    def key(self) -> str:
        return ""
