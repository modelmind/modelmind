from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException

from modelmind.config import settings
from modelmind.db.daos.sessions import SessionsDAO
from modelmind.db.schemas import DBIdentifier
from modelmind.db.schemas.sessions import DBCreateSession, SessionStatus


def create_jwt_session_token(session_id: DBIdentifier, profile_id: DBIdentifier) -> str:
    payload = {
        "session": str(session_id),
        "profile": str(profile_id),
        "exp": datetime.utcnow() + timedelta(minutes=settings.jwt.session_timeout_minutes),
    }
    return jwt.encode(payload, settings.jwt.secret_key, algorithm=settings.jwt.algorithm)


async def create_session(
    profile_id: DBIdentifier, questionnaire_id: DBIdentifier, language: str, metadata: dict
) -> DBIdentifier:
    try:
        return (
            await SessionsDAO.create(
                DBCreateSession(
                    profile_id=profile_id,
                    questionnaire_id=questionnaire_id,
                    status=SessionStatus.IN_PROGRESS,
                    language=language,
                    metadata=metadata,
                )
            )
        ).id
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
