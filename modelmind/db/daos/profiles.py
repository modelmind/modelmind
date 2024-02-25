from uuid import UUID

from modelmind.db.exceptions.profiles import ProfileNotFound
from modelmind.db.firestore import firestore_client as db
from modelmind.db.schemas.profiles import CreateProfile, DBIdentifierUUID, DBProfile

from .base import FirestoreDAO


class ProfilesDAO(FirestoreDAO[DBProfile]):
    _collection_name = "profiles"

    @classmethod
    async def create_profile(cls) -> DBIdentifierUUID:
        profile = CreateProfile()
        await cls.add(profile.model_dump(), str(profile.id))
        return UUID(profile.id)

    @classmethod
    async def get_from_id(cls, profile_id: str) -> DBProfile:
        try:
            return await cls.get(profile_id)
        except Exception:
            raise ProfileNotFound()
