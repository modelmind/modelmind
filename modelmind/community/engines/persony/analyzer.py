from pydantic import BaseModel

from modelmind.community.engines.persony.dimensions import PersonyDimension
from modelmind.community.theory.jung.functions import JungFunctionsAnalytics
from modelmind.community.theory.mbti.trait import MBTITraitsAnalytics
from modelmind.models.analytics.base import BaseAnalytics
from modelmind.models.questions import QuestionKey
from modelmind.models.results import Result

from .questions import PersonyQuestion


class PersonyAnalyzer:
    class Config(BaseModel):
        neutral_addition: int = 1

    def __init__(self, config: Config, question_key_mapping: dict[QuestionKey, PersonyQuestion]) -> None:
        self.config = config
        self.question_key_mapping = question_key_mapping
        self.base_mbti_analytics = MBTITraitsAnalytics(complexity=MBTITraitsAnalytics.Complexity.basic)
        self.advanced_mbti_analytics = MBTITraitsAnalytics(complexity=MBTITraitsAnalytics.Complexity.advanced)
        self.jung_analytics = JungFunctionsAnalytics()

    def add_traits_and_functions(self, dimension: PersonyDimension, value: int) -> None:
        if value < 0:
            self._handle_negative_value(dimension, value)
        elif value > 0:
            self._handle_positive_value(dimension, value)
        else:
            self._handle_neutral_value(dimension)

    def _handle_negative_value(self, dimension: PersonyDimension, value: int) -> None:
        if dimension.low_trait:
            if not dimension.has_function:
                self.base_mbti_analytics.add(dimension.low_trait, abs(value))
            self.advanced_mbti_analytics.add(dimension.low_trait, abs(value))
        if dimension.low_function:
            self.jung_analytics.add(dimension.low_function, abs(value))

    def _handle_positive_value(self, dimension: PersonyDimension, value: int) -> None:
        if dimension.high_trait:
            if not dimension.has_function:
                self.base_mbti_analytics.add(dimension.high_trait, value)
            self.advanced_mbti_analytics.add(dimension.high_trait, value)
        if dimension.high_function:
            self.jung_analytics.add(dimension.high_function, value)

    def _handle_neutral_value(self, dimension: PersonyDimension) -> None:
        if dimension.low_trait and dimension.high_trait:
            self.advanced_mbti_analytics.add(dimension.low_trait, self.config.neutral_addition)
            self.advanced_mbti_analytics.add(dimension.high_trait, self.config.neutral_addition)
            if not dimension.has_function:
                self.base_mbti_analytics.add(dimension.low_trait, self.config.neutral_addition)
                self.base_mbti_analytics.add(dimension.high_trait, self.config.neutral_addition)
        if dimension.low_function and dimension.high_function:
            self.jung_analytics.add(dimension.low_function, self.config.neutral_addition)
            self.jung_analytics.add(dimension.high_function, self.config.neutral_addition)

    def calculate_analytics(self, current_result: Result) -> list[BaseAnalytics]:
        """Build the analytics for the current result."""

        for question_key, value in current_result.data.items():
            question = self.question_key_mapping.get(question_key)
            if question is None:
                continue

            dimension = PersonyDimension(question.category)
            self.add_traits_and_functions(dimension, value)

        return [self.base_mbti_analytics, self.advanced_mbti_analytics, self.jung_analytics]
