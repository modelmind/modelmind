import logging
from typing import Optional

from fastapi import Depends, HTTPException

from modelmind.api.public.dependencies.daos.providers import profiles_dao_provider
from modelmind.api.public.dependencies.session.get import get_jwt_payload_from_token, get_next_payload_from_cookies
from modelmind.api.public.exceptions.jwt import JWTExpiredException, JWTMissingException
from modelmind.db.daos.profiles import ProfilesDAO
from modelmind.db.exceptions.profiles import DBProfileNotFound
from modelmind.db.schemas import DBIdentifier
from modelmind.db.schemas.profiles import DBProfile


def get_profile_id_from_token(
    session_payload: dict = Depends(get_jwt_payload_from_token),
    next_payload: dict | None = Depends(get_next_payload_from_cookies),
) -> DBIdentifier | None:
    try:
        if next_payload:
            return next_payload.get("profileId")
        return session_payload.get("profile")
    except JWTMissingException:
        return None
    except JWTExpiredException:
        return None


async def get_profile(
    profile_id: DBIdentifier | None = Depends(get_profile_id_from_token),
    profiles_dao: ProfilesDAO = Depends(profiles_dao_provider),
) -> DBProfile:
    if profile_id is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    else:
        try:
            return await profiles_dao.get_from_id(profile_id)
        except DBProfileNotFound as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            logging.error(f"Error getting profile: {e}")
            raise HTTPException(status_code=500, detail=str(e))


async def get_profile_optional(
    profile_id: DBIdentifier | None = Depends(get_profile_id_from_token),
    profiles_dao: ProfilesDAO = Depends(profiles_dao_provider),
) -> Optional[DBProfile]:
    if profile_id is None:
        return None
    else:
        try:
            return await profiles_dao.get_from_id(profile_id)
        except DBProfileNotFound:
            return None
        except Exception as e:
            logging.error(f"Error getting profile: {e}")
            raise HTTPException(status_code=500, detail=str(e))


async def get_or_create_profile(
    profile_id: DBIdentifier | None = Depends(get_profile_id_from_token),
    profiles_dao: ProfilesDAO = Depends(profiles_dao_provider),
) -> DBProfile:
    if profile_id is None:
        profile = await profiles_dao.create()
        return await profiles_dao.get_from_id(profile.id)
    else:
        try:
            return await profiles_dao.get_from_id(profile_id)
        except DBProfileNotFound:
            profile = await profiles_dao.create()
            return await profiles_dao.get_from_id(profile.id)
        except Exception as e:
            logging.error(f"Error getting profile: {e}")
            raise HTTPException(status_code=500, detail=str(e))
