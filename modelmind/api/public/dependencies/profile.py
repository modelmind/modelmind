from typing import Optional

from fastapi import Depends, Header, HTTPException

from modelmind.db.daos.profiles import ProfilesDAO
from modelmind.db.exceptions.profiles import ProfileNotFound
from modelmind.db.schemas.profiles import DBProfile


def get_profile_id(profile_id: Optional[str] = Header(None)) -> Optional[str]:
    return profile_id


async def get_profile(profile_id: str = Depends(get_profile_id)) -> DBProfile:
    if profile_id is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    else:
        try:
            return await ProfilesDAO.get_from_id(profile_id)
        except ProfileNotFound as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


async def get_or_create_profile(profile_id: str = Depends(get_profile_id)) -> DBProfile:
    if profile_id is None:
        profile_uuid = await ProfilesDAO.create_profile()
        return await ProfilesDAO.get_from_id(str(profile_uuid))
    else:
        try:
            return await ProfilesDAO.get_from_id(profile_id)
        except ProfileNotFound:
            profile_uuid = await ProfilesDAO.create_profile()
            return await ProfilesDAO.get_from_id(str(profile_uuid))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
