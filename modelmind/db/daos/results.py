from typing import List
from uuid import UUID

from .base import FirestoreDAO
from db.firestore import firestore_client as db
from db.schemas import DBObject
from db.schemas.results import DBResult


class ResultsDAO(FirestoreDAO[DBResult]):

    _collection_name = "results"
