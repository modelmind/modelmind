from typing import Any
from fastapi import Body, Depends, HTTPException
import logging
from modelmind.api.public.dependencies.session.get import get_session_from_token
from modelmind.db.daos.results import ResultsDAO
from modelmind.db.schemas.sessions import DBSession
from modelmind.models.results.base import Result


def get_result(data: Any = Body(..., description="The current results data of the questionnaire")) -> Result:
    try:
        print("data=", data)
        return Result(data={})
    except Exception as e:
        logging.error(f"Failed to create result: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


async def get_result_from_session(session: DBSession = Depends(get_session_from_token)) -> Result:
    try:
        db_result = await ResultsDAO.get_result_from_session_id(session.id)
        return Result(data=db_result.data)
    except Exception as e:
        logging.error(f"Failed to fetch result from session {session.id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
