from pydantic import BaseModel

from modelmind.community.engines.persony.dimensions import PersonyDimension
from modelmind.community.theory.jung.functions import JungFunctionsAnalytics
from modelmind.community.theory.mbti.trait import MBTITraitsAnalytics
from modelmind.community.theory.mbti.types import MBTIType
from modelmind.community.theory.neuroticism.trait import NeuroticismAnalytics
from modelmind.logger import log
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
        self.init_analytics()

    def init_analytics(self) -> None:
        self.base_mbti_analytics = MBTITraitsAnalytics(complexity=MBTITraitsAnalytics.Complexity.basic)
        self.advanced_mbti_analytics = MBTITraitsAnalytics(complexity=MBTITraitsAnalytics.Complexity.advanced)
        self.jung_analytics = JungFunctionsAnalytics()
        self.neuroticism_analytics = NeuroticismAnalytics()

    def _add_traits_and_functions(self, dimension: PersonyDimension, value: int, max_value: int) -> None:
        if value < 0:
            self._handle_negative_value(dimension, value, max_value)
        elif value > 0:
            self._handle_positive_value(dimension, value, max_value)
        else:
            self._handle_neutral_value(dimension, max_value)

    def _handle_negative_value(self, dimension: PersonyDimension, value: int, max_value: int) -> None:
        if dimension.low_trait:
            if not dimension.has_function:
                self.base_mbti_analytics.add(dimension.low_trait, abs(value))
            self.advanced_mbti_analytics.add(dimension.low_trait, abs(value))
        if dimension.low_function:
            self.jung_analytics.add(dimension.low_function, abs(value), max_value=max_value)
        if dimension.high_function:
            self.jung_analytics.add(dimension.high_function, 0, max_value=max_value)
        if dimension.low_neuroticism:
            self.neuroticism_analytics.add(dimension.low_neuroticism, abs(value), max_value=max_value)

    def _handle_positive_value(self, dimension: PersonyDimension, value: int, max_value: int) -> None:
        if dimension.high_trait:
            if not dimension.has_function:
                self.base_mbti_analytics.add(dimension.high_trait, value)
            self.advanced_mbti_analytics.add(dimension.high_trait, value)
        if dimension.low_function:
            self.jung_analytics.add(dimension.low_function, 0, max_value=max_value)
        if dimension.high_function:
            self.jung_analytics.add(dimension.high_function, value, max_value=max_value)
        if dimension.high_neuroticism:
            self.neuroticism_analytics.add(dimension.high_neuroticism, value, max_value=max_value)

    def _handle_neutral_value(self, dimension: PersonyDimension, max_value: int) -> None:
        if dimension.low_trait and dimension.high_trait:
            self.advanced_mbti_analytics.add(dimension.low_trait, self.config.neutral_addition)
            self.advanced_mbti_analytics.add(dimension.high_trait, self.config.neutral_addition)
            if not dimension.has_function:
                self.base_mbti_analytics.add(dimension.low_trait, self.config.neutral_addition)
                self.base_mbti_analytics.add(dimension.high_trait, self.config.neutral_addition)
        if dimension.low_function and dimension.high_function:
            self.jung_analytics.add(dimension.low_function, self.config.neutral_addition, max_value)
            self.jung_analytics.add(dimension.high_function, self.config.neutral_addition, max_value)
        if dimension.low_neuroticism and dimension.high_neuroticism:
            self.neuroticism_analytics.add(dimension.low_neuroticism, self.config.neutral_addition, max_value)
            self.neuroticism_analytics.add(dimension.high_neuroticism, self.config.neutral_addition, max_value)

    def calculate_analytics(self, current_result: Result) -> list[BaseAnalytics]:
        """Build the analytics for the current result."""

        self.init_analytics()

        for question_key, value in current_result.data.items():
            question = self.question_key_mapping.get(question_key)
            if question is None:
                log.warning("Analyzer: question with key %s not found", question_key)
                continue

            dimension = PersonyDimension(question.category)
            value = -value if question.question.reversed else value
            self._add_traits_and_functions(dimension, value, question.question.max)

        return [self.base_mbti_analytics, self.advanced_mbti_analytics, self.jung_analytics]

    @staticmethod
    def find_base_analytics(analytics: list[BaseAnalytics]) -> MBTITraitsAnalytics | None:
        """Find the base MBTI analytics in the list of analytics."""
        for analytic in analytics:
            if (
                isinstance(analytic, MBTITraitsAnalytics)
                and analytic.complexity == MBTITraitsAnalytics.Complexity.basic
            ):
                return analytic
        return None

    @staticmethod
    def find_advanced_analytics(analytics: list[BaseAnalytics]) -> MBTITraitsAnalytics | None:
        """Find the advanced MBTI analytics in the list of analytics."""
        for analytic in analytics:
            if (
                isinstance(analytic, MBTITraitsAnalytics)
                and analytic.complexity == MBTITraitsAnalytics.Complexity.advanced
            ):
                return analytic
        return None

    def calculate_dominants(self, current_result: Result) -> MBTIType:
        """Get the dominant MBTI type from the current result."""

        analytics = self.calculate_analytics(current_result)
        advanced_analytics = self.find_advanced_analytics(analytics)
        if advanced_analytics:
            return advanced_analytics.dominants
        else:
            raise ValueError("Advanced MBTI analytics not found")
