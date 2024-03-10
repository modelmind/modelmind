from fastapi import Depends

from modelmind.api.public.exceptions.sessions import (
    SessionAlreadyCompletedException,
    SessionExpiredException,
    SessionInProgressException,
    UnknownSessionStatusException,
)
from modelmind.db.schemas.sessions import DBSession, SessionStatus

from .get import get_session_from_token


async def session_not_expired(session: DBSession = Depends(get_session_from_token)) -> DBSession:
    if session.status != SessionStatus.EXPIRED:
        return session
    else:
        raise SessionExpiredException(str(session.id))


async def session_status_in_progress(session: DBSession = Depends(get_session_from_token)) -> DBSession:
    if session.status == SessionStatus.IN_PROGRESS:
        return session
    elif session.status == SessionStatus.COMPLETED:
        raise SessionAlreadyCompletedException(str(session.id))
    elif session.status == SessionStatus.EXPIRED:
        raise SessionExpiredException(str(session.id))
    else:
        raise UnknownSessionStatusException()


async def session_status_completed(session: DBSession = Depends(get_session_from_token)) -> DBSession:
    if session.status == SessionStatus.COMPLETED:
        return session
    elif session.status == SessionStatus.IN_PROGRESS:
        raise SessionInProgressException(str(session.id))
    elif session.status == SessionStatus.EXPIRED:
        raise SessionExpiredException(str(session.id))
    else:
        raise UnknownSessionStatusException()
