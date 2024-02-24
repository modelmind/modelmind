from db.exceptions.sessions import SessionNotFound
from db.firestore import firestore_client as db
from db.schemas import DBIdentifierUUID
from db.schemas.sessions import DBCreateSession, DBSession, SessionStatus

from .base import FirestoreDAO


class SessionsDAO(FirestoreDAO[DBSession]):
    _collection_name = "sessions"

    @classmethod
    async def create(self, session: DBCreateSession) -> DBIdentifierUUID:
        await db.collection(self.collection_name).add(session.model_dump())[1]
        return session.id

    @classmethod
    async def update_status(self, session_id: DBIdentifierUUID, status: SessionStatus) -> None:
        try:
            await db.collection(self.collection_name).document(session_id).update({"status": status})
        except Exception as e:
            raise SessionNotFound(f"Session {session_id} not found: {str(e)}")
