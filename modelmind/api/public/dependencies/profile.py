import logging
from typing import Optional

import jwt
from fastapi import Depends, Header, HTTPException, Request

from modelmind.config import settings
from modelmind.db.daos.profiles import ProfilesDAO
from modelmind.db.exceptions.profiles import DBProfileNotFound
from modelmind.db.schemas import DBIdentifier
from modelmind.db.schemas.profiles import DBProfile


def get_profile_id_from_token(request: Request) -> Optional[DBIdentifier]:
    session_token = request.cookies.get("MM_PROFILE_ID")

    if session_token is None:
        return None
    try:
        payload = jwt.decode(session_token, settings.jwt.secret_key, algorithms=[settings.jwt.algorithm])
        return payload.get("profile")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Unauthorized")


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
