from google.cloud.firestore import ArrayUnion, AsyncClient

from modelmind.db.exceptions.profiles import DBProfileCreationFailed, DBProfileNotFound
from modelmind.db.schemas.profiles import CreateProfile, DBIdentifier, DBProfile

from .base import FirestoreDAO


class ProfilesDAO(FirestoreDAO[DBProfile]):
    _collection_name = "profiles"
    model = DBProfile

    def __init__(self, client: AsyncClient) -> None:
        super().__init__(client)

    async def create(self) -> DBProfile:
        try:
            return await self.add(CreateProfile().model_dump())
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
