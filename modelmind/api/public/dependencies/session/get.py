import jwt
from fastapi import Depends, Header, HTTPException

from modelmind.config import settings
from modelmind.db.daos.sessions import SessionsDAO
from modelmind.db.exceptions.sessions import SessionNotFound
from modelmind.db.schemas import DBIdentifier
from modelmind.db.schemas.sessions import DBSession


def get_session_id_from_token(x_session_token: str = Header(...)) -> DBIdentifier:
    try:
        payload = jwt.decode(x_session_token, settings.jwt.secret_key, algorithms=[settings.jwt.algorithm])
        return payload.get("sub")
    except jwt.PyJWTError:
        raise HTTPException(status_code=403, detail="Invalid token")


async def get_session_from_id(session_id: DBIdentifier) -> DBSession:
    try:
        return await SessionsDAO.get(session_id)
    except SessionNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


async def get_session_from_token(session_id: DBIdentifier = Depends(get_session_id_from_token)) -> DBSession:
    try:
        return await get_session_from_id(session_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid token")
