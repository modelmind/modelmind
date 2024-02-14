from typing import List
from uuid import UUID

from .base import FirestoreDAO
from modelmind.services.firestore import firestore_client as db
from modelmind.db.schemas.firestore import Document


class QuestionnairesDAO(FirestoreDAO):
    collection_name = "questionnaires"

    def get(self, result_id: UUID) -> None:
        ...
