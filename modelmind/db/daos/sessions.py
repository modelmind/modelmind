from .base import FirestoreDAO
from modelmind.db.firestore import firestore_client as db
from modelmind.db.schemas import DBIdentifierUUID
from modelmind.db.schemas.sessions import DBSession, SessionStatus, DBCreateSession, DBUpdateSession
from modelmind.db.exceptions.sessions import SessionNotFound

class SessionsDAO(FirestoreDAO[DBSession]):
    _collection_name = "sessions"


    @classmethod
    async def create(self, session: DBCreateSession) -> DBIdentifierUUID:
        await (db.collection(self.collection_name).add(session.model_dump()))[1]
        return session.id
