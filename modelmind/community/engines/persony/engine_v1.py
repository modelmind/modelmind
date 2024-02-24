from enum import StrEnum
from typing import Dict, List, Optional

from pydantic import BaseModel

from modelmind.community.engines.exceptions import EngineException
from modelmind.community.engines.persony.dimensions import PersonyDimension
from modelmind.community.theory.jung.functions import JungFunctionsAnalytics
from modelmind.community.theory.mbti.trait import MBTITrait, MBTITraitsAnalytics
from modelmind.community.theory.mbti.types import MBTIType
from modelmind.models.analytics.base import BaseAnalytics
from modelmind.models.engines.base import Engine
from modelmind.models.questions import Question, QuestionKey
from modelmind.models.results import Result
from modelmind.utils.type_adapter import TypeAdapter


class PersonyQuestion(Question):
    category: PersonyDimension


class PersonyEngineV1(Engine[PersonyQuestion]):
    class Config(BaseModel):
        neutral_addition: int = 1
        questions_count: dict[str, int] = {
            "PREFERENCES": 32,
            "LIFESTYLE": 16,
            "TEMPERAMENT": 16,
            "ATTITUDE": 8,
        }

    class AnalyticsType(StrEnum):
        BASE_MBTI_TRAITS = "BASE_MBTI_TRAITS"
        ADVANCED_MBTI_TRAITS = "ADVANCED_MBTI_TRAITS"
        JUNG_FUNCTIONS = "JUNG_FUNCTIONS"

    class Step(StrEnum):
        PREFERENCES = "PREFERENCES"
        LIFESTYLE = "LIFESTYLE"
        TEMPERAMENT = "TEMPERAMENT"
        ATTITUDE = "ATTITUDE"
        COMPLETED = "COMPLETED"

        @classmethod
        def get_step(cls, question_category: PersonyDimension) -> "PersonyEngineV1.Step":
            if question_category in PersonyDimension.preferences():
                return cls.PREFERENCES
            if question_category in PersonyDimension.lifestyles():
                return cls.LIFESTYLE
            if question_category in PersonyDimension.temperaments():
                return cls.TEMPERAMENT
            if question_category in PersonyDimension.attitudes():
                return cls.ATTITUDE
            raise InvalidQuestionCategory(f"Question category {question_category} not supported.")

    def __init__(self, questions: list[PersonyQuestion], config: "Config") -> None:
        self.questions = questions
        self.config = config
        self._question_step_mapping = self._create_question_step_mapping(questions)

    def _create_question_step_mapping(self, questions: List[PersonyQuestion]) -> Dict[Step, List[PersonyQuestion]]:
        """Preprocess the questions list to create a step to question mapping."""
        step_mapping = dict()  # type: ignore
        for question in questions:
            step = self.Step.get_step(question.category)
            step_mapping[step] = step_mapping.get(step, []) + [question]
        return step_mapping

    def get_questions_counts_by_step(self, current_result: Result) -> dict[Step, int]:
        counts = dict()  # type: ignore
        for question_key, value in current_result.data.items():
            question = self.get_question_by_key(question_key)
            if question is None:
                continue
            step = self.Step.get_step(question.category)
            counts[step] = counts.get(step, 0) + 1
        return counts

    def get_question_by_key(self, key: QuestionKey) -> PersonyQuestion | None:
        """Returns the Question object for the given key, or None if not found."""
        return self._question_key_mapping.get(key)

    def build_analytics(self, current_result: Result) -> list[BaseAnalytics]:
        """Build the analytics for the current result."""
        base_mbti_analytics = MBTITraitsAnalytics(complexity=MBTITraitsAnalytics.Complexity.basic)
        advanced_mbti_analytics = MBTITraitsAnalytics(complexity=MBTITraitsAnalytics.Complexity.advanced)
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
                if dimension.low_trait and not dimension.has_function:
                    base_mbti_analytics.add(dimension.low_trait, abs(value))
                if dimension.low_trait:
                    advanced_mbti_analytics.add(dimension.low_trait, abs(value))
                if dimension.low_function:
                    jung_analytics.add(dimension.low_function, abs(value))
            elif value > 0:
                # If the value is positive, we increase the high trait/function
                if dimension.high_trait and not dimension.has_function:
                    base_mbti_analytics.add(dimension.high_trait, value)
                if dimension.high_trait:
                    advanced_mbti_analytics.add(dimension.high_trait, value)
                if dimension.high_function:
                    jung_analytics.add(dimension.high_function, value)
            else:
                # If the value is neutral (0), we increase for both traits/functions
                if dimension.low_trait and dimension.high_trait and not dimension.has_function:
                    base_mbti_analytics.add(dimension.low_trait, self.config.neutral_addition)
                    base_mbti_analytics.add(dimension.high_trait, self.config.neutral_addition)
                if dimension.low_trait and dimension.high_trait:
                    advanced_mbti_analytics.add(dimension.low_trait, self.config.neutral_addition)
                    advanced_mbti_analytics.add(dimension.high_trait, self.config.neutral_addition)
                if dimension.low_function and dimension.high_function:
                    jung_analytics.add(dimension.low_function, self.config.neutral_addition)
                    jung_analytics.add(dimension.high_function, self.config.neutral_addition)

        return [base_mbti_analytics, advanced_mbti_analytics, jung_analytics]

    def get_current_step(self, current_result: Result) -> Step:
        counts = self.get_questions_counts_by_step(current_result)

        if counts.get(self.Step.PREFERENCES, 0) < self.config.questions_count[self.Step.PREFERENCES]:
            return self.Step.PREFERENCES
        elif counts.get(self.Step.LIFESTYLE, 0) < self.config.questions_count[self.Step.LIFESTYLE]:
            return self.Step.LIFESTYLE
        elif counts.get(self.Step.TEMPERAMENT, 0) < self.config.questions_count[self.Step.TEMPERAMENT]:
            return self.Step.TEMPERAMENT
        elif counts.get(self.Step.ATTITUDE, 0) < self.config.questions_count[self.Step.ATTITUDE]:
            return self.Step.ATTITUDE
        else:
            return self.Step.COMPLETED

    def _get_remaining_questions_by_category(
        self, category: PersonyDimension, current_result: Result
    ) -> List[PersonyQuestion]:
        return [
            question
            for question in self.questions
            if question.category == category and question.key not in current_result.data
        ]

    def _get_preferences_questions(
        self, current_result: Result, max_questions: Optional[int] = None
    ) -> List[PersonyQuestion]:
        return (
            self._get_remaining_questions_by_category(PersonyDimension.PREFERENCE_IE, current_result)[:max_questions]
            + self._get_remaining_questions_by_category(PersonyDimension.PREFERENCE_NS, current_result)[:max_questions]
            + self._get_remaining_questions_by_category(PersonyDimension.PREFERENCE_TF, current_result)[:max_questions]
            + self._get_remaining_questions_by_category(PersonyDimension.PREFERENCE_JP, current_result)[:max_questions]
        )

    def _get_lifestyle_questions(
        self, current_result: Result, dominants: MBTIType, max_questions: Optional[int] = None
    ) -> List[PersonyQuestion]:
        if MBTITrait.N + MBTITrait.T in dominants:
            return (
                self._get_remaining_questions_by_category(PersonyDimension.LIFESTYLE_NINE, current_result)[
                    :max_questions
                ]
                + self._get_remaining_questions_by_category(PersonyDimension.LIFESTYLE_TETI, current_result)[
                    :max_questions
                ]
            )
        elif MBTITrait.N + MBTITrait.F in dominants:
            return (
                self._get_remaining_questions_by_category(PersonyDimension.LIFESTYLE_NINE, current_result)[
                    :max_questions
                ]
                + self._get_remaining_questions_by_category(PersonyDimension.LIFESTYLE_FEFI, current_result)[
                    :max_questions
                ]
            )
        elif MBTITrait.S + MBTITrait.T in dominants:
            return (
                self._get_remaining_questions_by_category(PersonyDimension.LIFESTYLE_SISE, current_result)[
                    :max_questions
                ]
                + self._get_remaining_questions_by_category(PersonyDimension.LIFESTYLE_TETI, current_result)[
                    :max_questions
                ]
            )
        elif MBTITrait.S + MBTITrait.F in dominants:
            return (
                self._get_remaining_questions_by_category(PersonyDimension.LIFESTYLE_SISE, current_result)[
                    :max_questions
                ]
                + self._get_remaining_questions_by_category(PersonyDimension.LIFESTYLE_FEFI, current_result)[
                    :max_questions
                ]
            )
        else:
            raise PersonyEngineException(f"[Lifestyle] Invalid dominants {dominants}.")

    def _get_temperament_questions(
        self, current_result: Result, dominants: MBTIType, max_questions: Optional[int] = None
    ) -> List[PersonyQuestion]:
        if MBTITrait.J in dominants:
            return (
                self._get_remaining_questions_by_category(PersonyDimension.TEMPERAMENT_NISI, current_result)[
                    :max_questions
                ]
                + self._get_remaining_questions_by_category(PersonyDimension.TEMPERAMENT_TEFE, current_result)[
                    :max_questions
                ]
            )
        elif MBTITrait.P in dominants:
            return (
                self._get_remaining_questions_by_category(PersonyDimension.TEMPERAMENT_NESE, current_result)[
                    :max_questions
                ]
                + self._get_remaining_questions_by_category(PersonyDimension.TEMPERAMENT_TIFI, current_result)[
                    :max_questions
                ]
            )
        else:
            raise PersonyEngineException(f"[Temperament] Invalid dominants {dominants}.")

    def _get_attitude_questions(
        self, current_result: Result, dominants: MBTIType, max_questions: Optional[int] = None
    ) -> List[PersonyQuestion]:
        if MBTITrait.N + MBTITrait.T + MBTITrait.J in dominants:
            return (
                self._get_remaining_questions_by_category(PersonyDimension.ATTITUDE_INJ, current_result)[:max_questions]
                + self._get_remaining_questions_by_category(PersonyDimension.ATTITUDE_ETJ, current_result)[
                    :max_questions
                ]
            )
        elif MBTITrait.N + MBTITrait.N + MBTITrait.J in dominants:
            return (
                self._get_remaining_questions_by_category(PersonyDimension.ATTITUDE_INJ, current_result)[:max_questions]
                + self._get_remaining_questions_by_category(PersonyDimension.ATTITUDE_EFJ, current_result)[
                    :max_questions
                ]
            )
        elif MBTITrait.S + MBTITrait.T + MBTITrait.J in dominants:
            return (
                self._get_remaining_questions_by_category(PersonyDimension.ATTITUDE_ISJ, current_result)[:max_questions]
                + self._get_remaining_questions_by_category(PersonyDimension.ATTITUDE_ETJ, current_result)[
                    :max_questions
                ]
            )
        elif MBTITrait.S + MBTITrait.F + MBTITrait.J in dominants:
            return (
                self._get_remaining_questions_by_category(PersonyDimension.ATTITUDE_ISJ, current_result)[:max_questions]
                + self._get_remaining_questions_by_category(PersonyDimension.ATTITUDE_EFJ, current_result)[
                    :max_questions
                ]
            )
        elif MBTITrait.N + MBTITrait.T + MBTITrait.P in dominants:
            return (
                self._get_remaining_questions_by_category(PersonyDimension.ATTITUDE_ITP, current_result)[:max_questions]
                + self._get_remaining_questions_by_category(PersonyDimension.ATTITUDE_ENP, current_result)[
                    :max_questions
                ]
            )
        elif MBTITrait.N + MBTITrait.F + MBTITrait.P in dominants:
            return (
                self._get_remaining_questions_by_category(PersonyDimension.ATTITUDE_IFP, current_result)[:max_questions]
                + self._get_remaining_questions_by_category(PersonyDimension.ATTITUDE_ENP, current_result)[
                    :max_questions
                ]
            )
        elif MBTITrait.S + MBTITrait.T + MBTITrait.P in dominants:
            return (
                self._get_remaining_questions_by_category(PersonyDimension.ATTITUDE_ITP, current_result)[:max_questions]
                + self._get_remaining_questions_by_category(PersonyDimension.ATTITUDE_ESP, current_result)[
                    :max_questions
                ]
            )
        elif MBTITrait.S + MBTITrait.F + MBTITrait.P in dominants:
            return (
                self._get_remaining_questions_by_category(PersonyDimension.ATTITUDE_IFP, current_result)[:max_questions]
                + self._get_remaining_questions_by_category(PersonyDimension.ATTITUDE_ESP, current_result)[
                    :max_questions
                ]
            )
        else:
            raise PersonyEngineException(f"[Attitude] Invalid dominants {dominants}.")

    def _get_advanced_mbti_analytics(self, analytics: list[BaseAnalytics]) -> MBTITraitsAnalytics:
        advanced_mbti_analytics = next(
            (a for a in analytics if isinstance(a, MBTITraitsAnalytics)
             and a.complexity == self.AnalyticsType.ADVANCED_MBTI_TRAITS), None
        )
        if not isinstance(advanced_mbti_analytics, MBTITraitsAnalytics):
            raise PersonyEngineException("Could not find advanced MBTI analytics.")
        return advanced_mbti_analytics

    async def infer_next_questions(self, current_result: Result) -> list[Question]:
        analytics = self.build_analytics(current_result)

        advanced_mbti_analytics = self._get_advanced_mbti_analytics(analytics)

        current_dominants = advanced_mbti_analytics.dominants

        current_step = self.get_current_step(current_result)

        if current_step == self.Step.PREFERENCES:
            max_questions = self.config.questions_count[self.Step.PREFERENCES] // 4
            questions = self._get_preferences_questions(current_result, max_questions)
        elif current_step == self.Step.LIFESTYLE:
            max_questions = self.config.questions_count[self.Step.LIFESTYLE] // 2
            questions = self._get_lifestyle_questions(current_result, current_dominants, max_questions)
        elif current_step == self.Step.TEMPERAMENT:
            max_questions = self.config.questions_count[self.Step.TEMPERAMENT] // 2
            questions = self._get_temperament_questions(current_result, current_dominants, max_questions)
        elif current_step == self.Step.ATTITUDE:
            max_questions = self.config.questions_count[self.Step.ATTITUDE] // 2
            questions = self._get_attitude_questions(current_result, current_dominants, max_questions)
        else:
            questions = []

        return TypeAdapter.validate(List[Question], questions)

    def is_completed(self, current_result: Result) -> bool:
        return self.get_current_step(current_result) == self.Step.COMPLETED


class PersonyEngineException(EngineException):
    pass


class InvalidQuestionCategory(PersonyEngineException):
    pass
