import logging
from typing import Optional

import jwt
from fastapi import Depends, HTTPException, Request, Response
from jwt.exceptions import InvalidSignatureError

from modelmind.api.public.dependencies.daos.providers import profiles_dao_provider
from modelmind.api.public.dependencies.session.get import get_next_payload_from_cookies
from modelmind.config import settings
from modelmind.db.daos.profiles import ProfilesDAO
from modelmind.db.exceptions.profiles import DBProfileNotFound
from modelmind.db.schemas import DBIdentifier
from modelmind.db.schemas.profiles import DBProfile
from modelmind.logger import log


def create_profile_token(profile_id: DBIdentifier) -> str:
    payload = {"id": str(profile_id), "iss": "modelmind", "aud": "modelmind"}
    return jwt.encode(payload, settings.jwt.secret_key, algorithm=settings.jwt.algorithm)


def decode_profile_token(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            settings.jwt.secret_key,
            algorithms=[settings.jwt.algorithm],
            audience="modelmind",
            issuer="modelmind",
        )
    except InvalidSignatureError as e:
        log.warning(f"Profile Token Error: {e}")
        raise HTTPException(status_code=401, detail="Invalid profile token") from e
    except jwt.PyJWTError as e:
        log.warning(f"Profile Token Error: {e}")
        raise HTTPException(status_code=401, detail="Could not decode profile token") from e


def get_profile_id_from_cookies(request: Request) -> DBIdentifier | None:
    profile_token = request.cookies.get(settings.mm_profile_cookie)

    if profile_token:
        return decode_profile_token(profile_token).get("id")

    return None


def get_profile_id_from_next_session(
    next_payload: dict | None = Depends(get_next_payload_from_cookies),
) -> DBIdentifier | None:
    if next_payload is None:
        return None
    return next_payload.get("profileId")


def get_profile_id(
    profile_id_from_cookies: DBIdentifier | None = Depends(get_profile_id_from_cookies),
    profile_id_from_next: DBIdentifier | None = Depends(get_profile_id_from_next_session),
) -> DBIdentifier | None:
    return profile_id_from_cookies or profile_id_from_next


async def get_profile(
    profile_id: DBIdentifier | None = Depends(get_profile_id),
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
    profile_id: DBIdentifier | None = Depends(get_profile_id),
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
    response: Response,
    profile_id: DBIdentifier | None = Depends(get_profile_id),
    profiles_dao: ProfilesDAO = Depends(profiles_dao_provider),
) -> DBProfile:
    if profile_id is None:
        profile = await profiles_dao.create()
        profile_token = create_profile_token(profile.id)
        response.set_cookie(settings.mm_profile_cookie, profile_token, domain=settings.domain)
        return await profiles_dao.get_from_id(profile.id)
    else:
        try:
            return await profiles_dao.get_from_id(profile_id)
        except DBProfileNotFound:
            profile = await profiles_dao.create(profile_id)
            log.critical(f"Profile {profile_id} not found, created new profile {profile.id}")
            return await profiles_dao.get_from_id(profile.id)
        except Exception as e:
            logging.error(f"Error getting profile: {e}")
            raise HTTPException(status_code=500, detail=str(e))
