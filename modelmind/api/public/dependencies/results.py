from fastapi import Body, Depends, HTTPException

from modelmind.api.public.dependencies.session.get import get_session_from_token
from modelmind.db.daos.results import ResultsDAO
from modelmind.db.schemas.sessions import DBSession
from modelmind.models.results.base import Result


def get_result(data: dict = Body(..., description="The current results data of the questionnaire")) -> Result:
    try:
        return Result(data=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_result_from_session(session: DBSession = Depends(get_session_from_token)) -> Result:
    try:
        return await ResultsDAO.get_result_from_session_id(session.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
