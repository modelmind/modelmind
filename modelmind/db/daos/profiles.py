from modelmind.db.exceptions.profiles import DBProfileCreationFailed, DBProfileNotFound
from modelmind.db.schemas.profiles import CreateProfile, DBIdentifier, DBProfile

from .base import FirestoreDAO


class ProfilesDAO(FirestoreDAO[DBProfile]):
    _collection_name = "profiles"
    model = DBProfile

    @classmethod
    async def create(self) -> DBProfile:
        try:
            return await self.add(CreateProfile().model_dump())
        except Exception:
            raise DBProfileCreationFailed()

    @classmethod
    async def get_from_id(self, profile_id: DBIdentifier) -> DBProfile:
        try:
            return await self.get(profile_id)
        except Exception:
            raise DBProfileNotFound()
