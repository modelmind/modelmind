from datetime import datetime
from typing import Optional
from uuid import uuid4

from google.cloud.firestore import ArrayUnion, AsyncClient

from modelmind.db.exceptions.profiles import DBProfileCreationFailed, DBProfileNotFound
from modelmind.db.schemas.profiles import Biographics, DBIdentifier, DBProfile

from .base import FirestoreDAO


class ProfilesDAO(FirestoreDAO[DBProfile]):
    _collection_name = "profiles"
    model = DBProfile

    def __init__(self, client: AsyncClient) -> None:
        super().__init__(client)

    async def create(self, profile_id: Optional[DBIdentifier] = None) -> DBProfile:
        try:
            profile_data = {
                "id": profile_id or str(uuid4()),
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            }
            return await self.add(profile_data)
        except Exception:
            raise DBProfileCreationFailed()

    async def get_from_id(self, profile_id: DBIdentifier) -> DBProfile:
        try:
            return await self.get(profile_id)
        except Exception:
            raise DBProfileNotFound()

    async def add_result(self, profile_id: DBIdentifier, result_id: DBIdentifier) -> None:
        try:
            await self.document_ref(profile_id).update({"results": ArrayUnion([result_id])})
        except Exception as e:
            raise e

    async def add_session(self, profile_id: DBIdentifier, session_id: DBIdentifier) -> None:
        try:
            await self.document_ref(profile_id).update({"sessions": ArrayUnion([session_id])})
        except Exception as e:
            raise e

    async def update_biographics(self, profile_id: DBIdentifier, biographics: Biographics) -> None:
        try:
            await self.update(profile_id, {"biographics": biographics})
        except Exception as e:
            raise e
