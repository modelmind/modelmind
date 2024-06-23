import logging

from fastapi import Body, Depends, HTTPException, Path, Query

from modelmind.api.public.dependencies.daos.providers import results_dao_provider
from modelmind.api.public.dependencies.profile import get_profile
from modelmind.api.public.dependencies.session.get import get_session_from_token
from modelmind.db.daos.results import ResultsDAO
from modelmind.db.exceptions.base import DBObjectNotFound
from modelmind.db.schemas.profiles import DBProfile
from modelmind.db.schemas.results import DBResult
from modelmind.db.schemas.sessions import DBSession
from modelmind.models.results.base import Result


def get_result(data: dict = Body(..., description="The current results data of the questionnaire")) -> Result:
    try:
        return Result(data=data)
    except Exception as e:
        logging.error(f"Failed to create result: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


async def get_result_from_id(
    result_id: str = Query(..., description="The result id"), results_dao: ResultsDAO = Depends(results_dao_provider)
) -> DBResult:
    try:
        return await results_dao.get(result_id)
    except Exception as e:
        logging.error(f"Failed to fetch result {result_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


async def get_result_from_path(
    result_id: str = Path(..., description="The result id"), results_dao: ResultsDAO = Depends(results_dao_provider)
) -> DBResult:
    try:
        return await results_dao.get(result_id)
    except DBObjectNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logging.error(f"Failed to fetch result {result_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


async def get_result_from_session(
    session: DBSession = Depends(get_session_from_token), results_dao: ResultsDAO = Depends(results_dao_provider)
) -> DBResult:
    try:
        return await results_dao.get_result_from_session_id(session.id)
    except Exception as e:
        logging.error(f"Failed to fetch result from session {session.id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


async def is_result_owner(
    db_result: DBResult = Depends(get_result_from_path), db_profile: DBProfile = Depends(get_profile)
) -> None:
    if db_result.id not in db_profile.results:
        raise HTTPException(status_code=403, detail="Not allowed to access this result")
