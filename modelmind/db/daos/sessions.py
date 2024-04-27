from datetime import datetime
from typing import Optional
from uuid import uuid4

from google.cloud.firestore import AsyncClient

from modelmind.db.exceptions.sessions import SessionNotFound
from modelmind.db.schemas import DBIdentifier
from modelmind.db.schemas.sessions import DBSession, DBUpdateSession, SessionStatus

from .base import FirestoreDAO


class SessionsDAO(FirestoreDAO[DBSession]):
    _collection_name = "sessions"
    model = DBSession

    def __init__(self, client: AsyncClient) -> None:
        super().__init__(client)

    async def create(
        self,
        profile_id: DBIdentifier,
        questionnaire_id: DBIdentifier,
        status: SessionStatus,
        language: str,
        id: Optional[DBIdentifier] = None,
        metadata: Optional[dict] = None,
    ) -> DBSession:
        if not id:
            id = str(uuid4())
        try:
            return await self.add(
                {
                    "id": id,
                    "profile_id": profile_id,
                    "questionnaire_id": questionnaire_id,
                    "status": status,
                    "language": language,
                    "metadata": metadata,
                    "created_at": datetime.now(),
                    "updated_at": datetime.now(),
                }
            )
        except Exception as e:
            # TODO: custom exception
            raise e

    async def update_status(self, session_id: DBIdentifier, status: SessionStatus) -> None:
        try:
            await self.update(session_id, DBUpdateSession(status=status).model_dump())
        except Exception as e:
            raise SessionNotFound(f"Session {session_id} not found: {str(e)}")
