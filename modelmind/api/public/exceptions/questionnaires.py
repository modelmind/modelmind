from modelmind.api.exceptions import NotFoundException


class QuestionnaireNotFoundException(NotFoundException):
    def __init__(self, name: str):
        detail = f"Questionnaire '{name}' not found."
        super().__init__(detail=detail)
