from uuid import UUID
from modelmind.db.daos.sessions import SessionsDAO
from modelmind.db.schemas.sessions import CreateSession, SessionStatus, SessionDocument
from modelmind.db.exceptions.sessions import SessionNotFound
from fastapi import Depends, HTTPException, Header
import jwt
from modelmind.config import settings
from datetime import datetime, timedelta



def create_jwt_session_token(session_id: UUID) -> str:
    payload = {
        "sub": str(session_id),
        "exp": datetime.utcnow() + timedelta(days=1),
    }
    return jwt.encode(payload, settings.jwt.secret_key, algorithm=settings.jwt.algorithm)


def verify_jwt_session_token(x_session_token: str = Header(...)) -> str:
    try:
        payload = jwt.decode(x_session_token, settings.jwt.secret_key, algorithms=[settings.jwt.algorithm])
        return payload.get("sub")
    except jwt.PyJWTError:
        raise HTTPException(status_code=403, detail="Invalid token")


async def get_session(session_id: str) -> SessionDocument:
    try:
        return await SessionsDAO.get(session_id)
    except SessionNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


async def create_session(questionnaire_id: str, language: str, metadata: dict) -> UUID:
    return await SessionsDAO.create(
        CreateSession(
            questionnaire_id=questionnaire_id,
            status=SessionStatus.IN_PROGRESS,
            language=language,
            metadata=metadata,
        )
    )


async def get_session_from_token(x_session_token: str = Depends(verify_jwt_session_token)) -> SessionDocument:
    return await get_session(x_session_token)
