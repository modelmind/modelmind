import jwt
from fastapi import Depends, HTTPException

from modelmind.api._dependencies.daos.providers import sessions_dao_provider
from modelmind.config import settings
from modelmind.db.daos.sessions import SessionsDAO
from modelmind.db.schemas import DBIdentifier
from modelmind.db.schemas.sessions import DBSession, SessionStatus


def create_jwt_session_token(session_id: DBIdentifier, profile_id: DBIdentifier) -> str:
    payload = {
        "session": str(session_id),
        "profile": str(profile_id),
    }
    return jwt.encode(payload, settings.jwt.secret_key, algorithm=settings.jwt.algorithm)


async def create_session(
    profile_id: DBIdentifier,
    questionnaire_id: DBIdentifier,
    language: str,
    metadata: dict,
    sessions_dao: SessionsDAO = Depends(sessions_dao_provider),
) -> DBSession:
    try:
        return await sessions_dao.create(
            profile_id=profile_id,
            questionnaire_id=questionnaire_id,
            status=SessionStatus.IN_PROGRESS,
            language=language,
            metadata=metadata,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
