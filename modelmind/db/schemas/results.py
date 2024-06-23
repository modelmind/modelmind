from enum import StrEnum

from . import DBIdentifier, DBObject


class DBResult(DBObject):
    questionnaire_id: DBIdentifier
    session_id: DBIdentifier

    data: dict

    class Visibility(StrEnum):
        PUBLIC = "public"
        PRIVATE = "private"

    visibility: Visibility = Visibility.PRIVATE
    label: str
