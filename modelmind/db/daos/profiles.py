from db.firestore import firestore_client as db
from db.schemas.profiles import DBProfile

from modelmind.db.exceptions.profiles import ProfileNotFound

from .base import FirestoreDAO


class ProfilesDAO(FirestoreDAO[DBProfile]):
    _collection_name = "profiles"

    @classmethod
    async def create_profile(cls) -> DBProfile:
        profile = DBProfile()
        profile.id = db.collection(cls._collection_name).document().id
        await db.collection(cls._collection_name).document(profile.id).set(profile.model_dump())
        return profile

    @classmethod
    async def get_from_id(cls, profile_id: str) -> DBProfile:
        try:
            doc = await db.collection(cls._collection_name).document(id).get()
            return DBProfile.model_validate(doc.to_dict())
        except Exception as e:
            raise ProfileNotFound()
