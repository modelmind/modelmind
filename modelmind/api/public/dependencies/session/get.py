import json
from datetime import datetime
from typing import Any, Dict, Optional

import jwt
from fastapi import Depends, HTTPException, Request
from hkdf import Hkdf
from jose.exceptions import JWEError
from jose.jwe import decrypt

from modelmind.api.public.dependencies.daos.providers import sessions_dao_provider
from modelmind.api.public.exceptions.jwt import JWTExpiredException, JWTInvalidException, JWTMissingException
from modelmind.config import settings
from modelmind.db.daos.sessions import SessionsDAO
from modelmind.db.exceptions.sessions import SessionNotFound
from modelmind.db.schemas import DBIdentifier
from modelmind.db.schemas.sessions import DBSession, SessionStatus
from modelmind.logger import log


def __next_encryption_key(secret: str) -> bytes:
    return Hkdf("", bytes(secret, "utf-8")).expand(b"NextAuth.js Generated Encryption Key", 32)


def decode_next_jwe(token: str, secret: str) -> Dict[str, Any]:
    decrypted = decrypt(token, __next_encryption_key(secret))

    if decrypted:
        return json.loads(bytes.decode(decrypted, "utf-8"))
    else:
        raise JWTInvalidException()


def get_next_payload_from_cookies(request: Request) -> Optional[dict]:
    session_token = request.cookies.get(settings.next_cookie)

    if session_token is None:
        return None
    try:
        payload = decode_next_jwe(session_token, settings.jwt.next_secret)
        if payload["exp"] < datetime.now().timestamp():
            log.exception("Next Cookie Error: JWT Expired for %s", payload.get("profileId"))
            raise JWTExpiredException()
        return payload
    except JWEError as e:
        log.warning("Next Cookie Error:", e)
        raise JWTInvalidException() from e


def get_session_payload_from_token(request: Request) -> dict:
    session_token = request.cookies.get(settings.mm_session_cookie)

    if session_token is None:
        raise JWTMissingException()
    try:
        return jwt.decode(session_token, settings.jwt.secret_key, algorithms=[settings.jwt.algorithm])
    except jwt.PyJWTError as e:
        log.warning("Session Cookie Error:", e)
        raise JWTInvalidException() from e


def get_session_id_from_token(jwt_payload: dict = Depends(get_session_payload_from_token)) -> DBIdentifier:
    return jwt_payload["session"]


async def get_session_from_id(
    session_id: DBIdentifier, sessions_dao: SessionsDAO = Depends(sessions_dao_provider)
) -> DBSession:
    try:
        return await sessions_dao.get(session_id)
    except SessionNotFound:
        raise HTTPException(status_code=403, detail="Forbidden")


async def fetch_session(session_id: DBIdentifier, sessions_dao: SessionsDAO) -> DBSession:
    session = await get_session_from_id(session_id, sessions_dao)
    if session.expires_at and session.expires_at < datetime.now():
        await sessions_dao.update_status(session_id, SessionStatus.EXPIRED)
        session.status = SessionStatus.EXPIRED
    return session


async def get_session_from_token(
    session_id: DBIdentifier = Depends(get_session_id_from_token),
    sessions_dao: SessionsDAO = Depends(sessions_dao_provider),
) -> DBSession:
    try:
        return await fetch_session(session_id, sessions_dao)
    except ValueError:
        raise HTTPException(status_code=403, detail="Forbidden")
