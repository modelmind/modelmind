import logging
from typing import Optional
from uuid import UUID

from fastapi import Depends, Header, HTTPException

from modelmind.db.daos.profiles import ProfilesDAO
from modelmind.db.exceptions.profiles import DBProfileNotFound
from modelmind.db.schemas.profiles import DBProfile


def get_profile_id(profile_id: Optional[UUID] = Header(None)) -> Optional[UUID]:
    return profile_id


async def get_profile(profile_id: UUID | None = Depends(get_profile_id)) -> DBProfile:
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


async def get_or_create_profile(profile_id: UUID | None = Depends(get_profile_id)) -> DBProfile:
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
