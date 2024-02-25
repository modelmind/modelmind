from modelmind.db.exceptions.sessions import SessionNotFound
from modelmind.db.schemas import DBIdentifier
from modelmind.db.schemas.sessions import DBCreateSession, DBSession, DBUpdateSession, SessionStatus

from .base import FirestoreDAO


class SessionsDAO(FirestoreDAO[DBSession]):
    _collection_name = "sessions"
    model = DBSession

    @classmethod
    async def create(self, session: DBCreateSession) -> DBSession:
        try:
            return await self.add(session.model_dump())
        except Exception as e:
            # TODO: custom exception
            raise e

    @classmethod
    async def update_status(self, session_id: DBIdentifier, status: SessionStatus) -> None:
        try:
            await self.update(session_id, DBUpdateSession(status=status).model_dump())
        except Exception as e:
            raise SessionNotFound(f"Session {session_id} not found: {str(e)}")
