from .base import FirestoreDAO
from db.firestore import firestore_client as db
from db.schemas.results import DBResult


class ProfilesDAO(FirestoreDAO[DBResult]):

    _collection_name = "profiles"
