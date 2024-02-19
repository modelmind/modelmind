from uuid import UUID

from .base import FirestoreDAO
from modelmind.services.firestore import firestore_client as db
from modelmind.db.schemas.sessions import SessionDocument, SessionStatus, CreateSession, UpdateSession
from modelmind.db.exceptions.sessions import SessionNotFound

class SessionsDAO(FirestoreDAO):
    collection_name = "sessions"

    @classmethod
    async def get(self, session_id: UUID | str) -> SessionDocument:
        doc_ref = db.collection(self.collection_name).document(str(session_id))
        doc = await doc_ref.get()
        if doc.exists:
            return SessionDocument.model_validate(doc.to_dict())
        else:
            raise SessionNotFound

    @classmethod
    async def create(self, session: CreateSession) -> UUID:
        await (db.collection(self.collection_name).add(session.model_dump()))[1]
        return session.uuid
