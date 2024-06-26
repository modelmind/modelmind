from typing import List, Optional, TypedDict

from . import DBIdentifier, DBObject


class MBTI(TypedDict, total=False):
    type: str
    confidence: float


class Enneagram(TypedDict, total=False):
    type: str
    wing: str
    tritype: str
    confidence: float


class BigFive(TypedDict, total=False):
    openness: float
    conscientiousness: float
    extraversion: float
    agreeableness: float
    neuroticism: float


class PersonalityBiographics(TypedDict, total=False):
    mbti: Optional[MBTI]
    enneagram: Optional[Enneagram]
    big_five: Optional[BigFive]


class Biographics(TypedDict, total=False):
    birth_year: Optional[int]
    gender: Optional[str]
    occupation: Optional[str]
    education: Optional[str]
    country: Optional[str]
    interests: Optional[List[str]]
    relationship_status: Optional[str]
    sexual_orientation: Optional[str]
    cultural_origin: Optional[str]
    income: Optional[str]
    religion: Optional[str]
    political_orientation: Optional[str]
    number_of_children: Optional[int]

    personality: Optional[PersonalityBiographics]


class DBProfile(DBObject):
    sessions: List[DBIdentifier] = []
    results: List[DBIdentifier] = []
    biographics: Biographics = {}
