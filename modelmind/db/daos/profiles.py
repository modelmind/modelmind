from modelmind.db.firestore import firestore_client as db
from modelmind.db.schemas.profiles import CreateProfile, DBProfile, DBIdentifierUUID

from modelmind.db.exceptions.profiles import ProfileNotFound

from .base import FirestoreDAO


class ProfilesDAO(FirestoreDAO[DBProfile]):
    _collection_name = "profiles"

    @classmethod
    async def create_profile(cls) -> DBIdentifierUUID:
        profile = CreateProfile()
        await db.collection(cls._collection_name).add(profile.model_dump())
        return profile.id

    @classmethod
    async def get_from_id(cls, profile_id: str) -> DBProfile:
        try:
            doc = await db.collection(cls._collection_name).document(id).get()
            return DBProfile.model_validate(doc.to_dict())
        except Exception:
            raise ProfileNotFound()
