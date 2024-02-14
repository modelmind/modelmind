from typing import List
from uuid import UUID

from .base import FirestoreDAO
from modelmind.services.firestore import firestore_client as db
from modelmind.db.schemas.firestore import Document


class ResultsDAO(FirestoreDAO):

    collection_name = "results"

    def get(self, questionnaire_id: str, result_id: UUID) -> None:
        ...
