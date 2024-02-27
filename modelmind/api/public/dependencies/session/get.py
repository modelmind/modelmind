import jwt
from fastapi import Depends, HTTPException, Request

from modelmind.config import settings
from modelmind.db.daos.sessions import SessionsDAO
from modelmind.db.exceptions.sessions import SessionNotFound
from modelmind.db.schemas import DBIdentifier
from modelmind.db.schemas.sessions import DBSession


def get_session_id_from_token(request: Request) -> DBIdentifier:
    session_token = request.cookies.get("MM_PROFILE_ID")

    if session_token is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        payload = jwt.decode(session_token, settings.jwt.secret_key, algorithms=[settings.jwt.algorithm])
        return payload.get("session")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Unauthorized")


async def get_session_from_id(session_id: DBIdentifier) -> DBSession:
    try:
        return await SessionsDAO.get(session_id)
    except SessionNotFound:
        raise HTTPException(status_code=403, detail="Forbidden")


async def get_session_from_token(session_id: DBIdentifier = Depends(get_session_id_from_token)) -> DBSession:
    try:
        return await get_session_from_id(session_id)
    except ValueError:
        raise HTTPException(status_code=403, detail="Forbidden")
