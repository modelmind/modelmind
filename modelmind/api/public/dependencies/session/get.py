from datetime import datetime

import jwt
from fastapi import Depends, HTTPException, Request

from modelmind.api.public.dependencies.daos.providers import sessions_dao_provider
from modelmind.api.public.exceptions.jwt import JWTExpiredException, JWTInvalidException, JWTMissingException
from modelmind.config import settings
from modelmind.db.daos.sessions import SessionsDAO
from modelmind.db.exceptions.sessions import SessionNotFound
from modelmind.db.schemas import DBIdentifier
from modelmind.db.schemas.sessions import DBSession


def get_jwt_payload_from_token(request: Request) -> dict:
    session_token = request.cookies.get("MM_PROFILE_ID")

    if session_token is None:
        raise JWTMissingException()
    try:
        payload = jwt.decode(session_token, settings.jwt.secret_key, algorithms=[settings.jwt.algorithm])
        if payload["exp"] < datetime.utcnow().timestamp():
            raise JWTExpiredException()
        return payload
    except jwt.PyJWTError as e:
        print(e)
        raise JWTInvalidException() from e


def get_session_id_from_token(request: Request) -> DBIdentifier:
    return get_jwt_payload_from_token(request)["session"]


async def get_session_from_id(
    session_id: DBIdentifier, sessions_dao: SessionsDAO = Depends(sessions_dao_provider)
) -> DBSession:
    try:
        return await sessions_dao.get(session_id)
    except SessionNotFound:
        raise HTTPException(status_code=403, detail="Forbidden")


async def get_session_from_token(
    session_id: DBIdentifier = Depends(get_session_id_from_token),
    sessions_dao: SessionsDAO = Depends(sessions_dao_provider),
) -> DBSession:
    try:
        return await get_session_from_id(session_id, sessions_dao)
    except ValueError:
        raise HTTPException(status_code=403, detail="Forbidden")
