from typing import List
from uuid import UUID

from .base import FirestoreDAO
from modelmind.db.firestore import firestore_client as db
from modelmind.db.schemas import DBObject


class ResultsDAO(FirestoreDAO):

    collection_name = "results"

    def get(self, questionnaire_id: str, result_id: UUID) -> None:
        ...
