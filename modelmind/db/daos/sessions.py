from google.cloud.firestore import AsyncClient

from modelmind.db.exceptions.sessions import SessionNotFound
from modelmind.db.schemas import DBIdentifier
from modelmind.db.schemas.sessions import DBCreateSession, DBSession, DBUpdateSession, SessionStatus

from .base import FirestoreDAO


class SessionsDAO(FirestoreDAO[DBSession]):
    _collection_name = "sessions"
    model = DBSession

    def __init__(self, client: AsyncClient) -> None:
        super().__init__(client)

    async def create(self, session: DBCreateSession) -> DBSession:
        try:
            return await self.add(session.model_dump())
        except Exception as e:
            # TODO: custom exception
            raise e

    async def update_status(self, session_id: DBIdentifier, status: SessionStatus) -> None:
        try:
            await self.update(session_id, DBUpdateSession(status=status).model_dump())
        except Exception as e:
            raise SessionNotFound(f"Session {session_id} not found: {str(e)}")
