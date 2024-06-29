from enum import StrEnum

from pydantic import Field

from . import DBIdentifier, DBObject


class DBResult(DBObject):
    questionnaire_id: DBIdentifier
    session_id: DBIdentifier
    profile_id: DBIdentifier = Field(default_factory=lambda: "unknown")

    data: dict

    class Visibility(StrEnum):
        PUBLIC = "public"
        PRIVATE = "private"

    visibility: Visibility = Visibility.PRIVATE
    label: str
    language: str | None = None
