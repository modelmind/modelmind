from typing import Dict, List
from modelmind.models.questions import Question, QuestionKey
from modelmind.models.questionnaires import Questionnaire
from modelmind.models.results import Result
from modelmind.models.engines.base import BaseEngine
from modelmind.community.theory.mbti.trait import MBTITrait, MBTITraitsAnalytics
from modelmind.community.theory.jung.functions import JungFunction, JungFunctionsAnalytics
from modelmind.community.engines.persony.dimensions import PersonyDimension


class PersonyEngineV1(BaseEngine):

    def __init__(self, questions: list[Question]) -> None:
        self.questions = questions
        self.question_key_mapping = self._create_question_key_mapping(questions)
        self.current_step = 0

    def _create_question_key_mapping(self, questions: List[Question]) -> Dict[QuestionKey, Question]:
        """Preprocess the questions list to create a key to question mapping."""
        return {question.key: question for question in questions}

    def get_question_by_key(self, key: QuestionKey) -> Question | None:
        """Returns the Question object for the given key, or None if not found."""
        return self.question_key_mapping.get(key)

    def build_analytics(self, current_result: Result) -> tuple[MBTITraitsAnalytics, JungFunctionsAnalytics]:
        """Build the analytics for the current result."""
        mbti_analytics = MBTITraitsAnalytics()
        jung_analytics = JungFunctionsAnalytics()

        for question_key, value in current_result.data.items():
            question = self.get_question_by_key(question_key)
            if question is None:
                continue

            # Instantiate the corresponding dimension to the question category
            # Contains mapping for low and high traits/functions
            dimension = PersonyDimension(question.category)

            if value < 0:
                # If the value is negative, we increase the low trait/function
                if dimension.low_trait:
                    mbti_analytics.add(dimension.low_trait, abs(value))
                if dimension.low_function:
                    jung_analytics.add(dimension.low_function, abs(value))
            elif value > 0:
                # If the value is positive, we increase the high trait/function
                if dimension.high_trait:
                    mbti_analytics.add(dimension.high_trait, value)
                if dimension.high_function:
                    jung_analytics.add(dimension.high_function, value)
            else:
                # If the value is neutral (0), we increase for both traits/functions
                if dimension.low_trait and dimension.high_trait:
                    mbti_analytics.add(dimension.low_trait, 1)
                    mbti_analytics.add(dimension.high_trait, 1)
                if dimension.low_function and dimension.high_function:
                    jung_analytics.add(dimension.low_function, 1)
                    jung_analytics.add(dimension.high_function, 1)

        return mbti_analytics, jung_analytics


    async def infer_next_questions(self, current_result: Result) -> list[Question]:

        mbti_analytics, jung_analytics = self.build_analytics(current_result)

        return []

