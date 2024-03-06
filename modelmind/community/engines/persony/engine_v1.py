import random
from enum import StrEnum
from typing import Dict, List, Optional

from pydantic import BaseModel

from modelmind.community.engines.exceptions import EngineException
from modelmind.community.engines.persony.dimensions import PersonyDimension
from modelmind.community.theory.mbti.trait import MBTITrait
from modelmind.community.theory.mbti.types import MBTIType
from modelmind.models.analytics.base import BaseAnalytics
from modelmind.models.engines.base import Engine
from modelmind.models.questions import Question
from modelmind.models.results import Result
from modelmind.utils.type_adapter import TypeAdapter

from .analyzer import PersonyAnalyzer
from .questions import PersonyQuestion


class PersonyEngineV1(Engine[PersonyQuestion]):
    class Config(BaseModel):
        neutral_addition: int = 1
        questions_count: dict[str, int] = {
            "PREFERENCES": 32,
            "LIFESTYLE": 16,
            "TEMPERAMENT": 16,
            "ATTITUDE": 8,
        }
        max_questions: int = 8

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

    def __init__(self, questions: list[PersonyQuestion], config: "Config" = Config()) -> None:
        super().__init__(questions)
        self.questions = questions
        self.config = config or self.Config()
        self.question_step_mapping = self._create_question_step_mapping(questions)
        self.analyzer = PersonyAnalyzer(
            config=PersonyAnalyzer.Config(neutral_addition=self.config.neutral_addition),
            question_key_mapping=self.question_key_mapping,
        )

    def get_questions_counts_by_step(self, current_result: Result) -> dict[Step, int]:
        counts = dict()  # type: ignore
        for question_key, _ in current_result.data.items():
            question = self.question_key_mapping.get(question_key)
            if question is None:
                continue
            step = self.Step.get_step(question.category)
            counts[step] = counts.get(step, 0) + 1
        return counts

    def build_analytics(self, current_result: Result) -> list[BaseAnalytics]:
        """Build the analytics for the current result."""
        return self.analyzer.calculate_analytics(current_result)

    def is_completed(self, current_result: Result) -> bool:
        return self.get_current_step(current_result) == self.Step.COMPLETED

    async def infer_next_questions(
        self, current_result: Result, max_questions: Optional[int], shuffle: bool = True
    ) -> List[Question]:
        self.build_analytics(current_result)

        advanced_mbti_analytics = self.analyzer.advanced_mbti_analytics

        current_dominants = advanced_mbti_analytics.dominants

        current_step = self.get_current_step(current_result)

        questions = self.select_remaining_questions_from_step(current_step, current_result, current_dominants)

        if shuffle:
            random.shuffle(questions)

        if not max_questions:
            max_questions = self.config.max_questions

        return TypeAdapter.validate(List[Question], questions[:max_questions])

    async def calculate_remaining_questions_count(self, current_result: Result) -> int:
        counts = self.get_questions_counts_by_step(current_result)
        remaining = 0
        for step in self.Step:
            if step == self.Step.COMPLETED:
                continue
            remaining += self.config.questions_count[step] - counts.get(step, 0)
        return remaining

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

    def select_remaining_questions_from_step(
        self, step: Step, current_result: Result, current_dominants: MBTIType
    ) -> List[PersonyQuestion]:
        if step == self.Step.PREFERENCES:
            max_questions = self.config.questions_count[self.Step.PREFERENCES] // 4
            questions = self._get_preferences_questions(current_result, max_questions)
        elif step == self.Step.LIFESTYLE:
            max_questions = self.config.questions_count[self.Step.LIFESTYLE] // 2
            questions = self._get_lifestyle_questions(current_result, current_dominants, max_questions)
        elif step == self.Step.TEMPERAMENT:
            max_questions = self.config.questions_count[self.Step.TEMPERAMENT] // 2
            questions = self._get_temperament_questions(current_result, current_dominants, max_questions)
        elif step == self.Step.ATTITUDE:
            max_questions = self.config.questions_count[self.Step.ATTITUDE] // 2
            questions = self._get_attitude_questions(current_result, current_dominants, max_questions)
        else:
            questions = []
        return questions

    def _create_question_step_mapping(self, questions: List[PersonyQuestion]) -> Dict[Step, List[PersonyQuestion]]:
        """Preprocess the questions list to create a step to question mapping."""
        step_mapping = dict()  # type: ignore
        for question in questions:
            step = self.Step.get_step(question.category)
            step_mapping[step] = step_mapping.get(step, []) + [question]
        return step_mapping

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


class PersonyEngineException(EngineException):
    pass


class InvalidQuestionCategory(PersonyEngineException):
    pass
