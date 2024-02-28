import logging
from typing import Optional

from fastapi import Depends, HTTPException, Request

from modelmind.api.public.dependencies.session.get import get_jwt_payload_from_token
from modelmind.api.public.exceptions.jwt import JWTExpiredException, JWTMissingException
from modelmind.db.daos.profiles import ProfilesDAO
from modelmind.db.exceptions.profiles import DBProfileNotFound
from modelmind.db.schemas import DBIdentifier
from modelmind.db.schemas.profiles import DBProfile


def get_profile_id_from_token(request: Request) -> Optional[DBIdentifier]:
    try:
        payload = get_jwt_payload_from_token(request)
        return payload.get("profile")
    except JWTMissingException:
        return None
    except JWTExpiredException:
        return None


async def get_profile(profile_id: DBIdentifier | None = Depends(get_profile_id_from_token)) -> DBProfile:
    if profile_id is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    else:
        try:
            return await ProfilesDAO.get_from_id(profile_id)
        except DBProfileNotFound as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            logging.error(f"Error getting profile: {e}")
            raise HTTPException(status_code=500, detail=str(e))


async def get_or_create_profile(profile_id: DBIdentifier | None = Depends(get_profile_id_from_token)) -> DBProfile:
    if profile_id is None:
        profile = await ProfilesDAO.create()
        return await ProfilesDAO.get_from_id(profile.id)
    else:
        try:
            return await ProfilesDAO.get_from_id(profile_id)
        except DBProfileNotFound:
            profile = await ProfilesDAO.create()
            return await ProfilesDAO.get_from_id(profile.id)
        except Exception as e:
            logging.error(f"Error getting profile: {e}")
            raise HTTPException(status_code=500, detail=str(e))
