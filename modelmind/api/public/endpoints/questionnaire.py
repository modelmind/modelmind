from fastapi import APIRouter, Depends, Response

from modelmind.api.public.dependencies.daos.providers import results_dao_provider, sessions_dao_provider
from modelmind.api.public.dependencies.profile import get_or_create_profile
from modelmind.api.public.dependencies.questionnaire import (
    get_questionnaire_by_name,
    initialize_questionnaire_from_session,
    validate_requested_language
)
from modelmind.api.public.dependencies.results import get_result, get_result_from_session
from modelmind.api.public.dependencies.session.create import create_jwt_session_token, create_session
from modelmind.api.public.dependencies.session.get import get_session_from_token
from modelmind.api.public.dependencies.session.verify import session_status_completed, session_status_in_progress
from modelmind.api.public.schemas.analytics import AnalyticsResponse
from modelmind.api.public.schemas.questionnaires import NextQuestionsResponse
from modelmind.api.public.schemas.results import ResultsResponse
from modelmind.db.daos.results import ResultsDAO
from modelmind.db.daos.sessions import SessionsDAO, SessionStatus
from modelmind.db.schemas.profiles import DBProfile
from modelmind.db.schemas.questionnaires import DBQuestionnaire
from modelmind.db.schemas.results import CreateResult
from modelmind.db.schemas.sessions import DBSession
from modelmind.models.questionnaires.base import Questionnaire
from modelmind.models.results.base import Result

router = APIRouter(prefix="/questionnaire")


@router.get("/{name}/{language}/session")
async def questionnaire_session_start(
    response: Response,
    language: str = Depends(validate_requested_language),
    questionnaire: DBQuestionnaire = Depends(get_questionnaire_by_name),
    profile: DBProfile = Depends(get_or_create_profile),
) -> Response:
    session_id = await create_session(profile.id, questionnaire.id, language, {})
    session_token = create_jwt_session_token(session_id)
    response.headers["x-session-token"] = session_token
    return Response(status_code=200)


@router.post(
    "/session/questions/next", response_model=NextQuestionsResponse, dependencies=[Depends(session_status_in_progress)]
)
async def questionnaire_session_questions_next(
    current_result: Result = Depends(get_result),
    questionnaire: Questionnaire = Depends(initialize_questionnaire_from_session),
    session: DBSession = Depends(get_session_from_token),
    sessions_dao: SessionsDAO = Depends(sessions_dao_provider),
    results_dao: ResultsDAO = Depends(results_dao_provider),
) -> NextQuestionsResponse:
    """Get the next questions for the current session and result"""

    if questionnaire.is_completed(current_result):
        await sessions_dao.update_status(session.id, SessionStatus.COMPLETED)
        await results_dao.save(
            CreateResult(session_id=session.id, questionnaire_id=session.questionnaire_id, data=current_result.data)
        )
        return NextQuestionsResponse(questions=[], completed=True)

    next_questions = await questionnaire.next_questions(current_result)

    return NextQuestionsResponse(questions=next_questions, completed=False)


@router.get("/session/results", response_model=ResultsResponse, dependencies=[Depends(session_status_completed)])
async def questionnaire_session_results(
    current_result: Result = Depends(get_result_from_session),
) -> ResultsResponse:
    return ResultsResponse(data=current_result.data)


@router.get("/session/analytics", response_model=AnalyticsResponse, dependencies=[Depends(session_status_completed)])
async def questionnaire_session_analytics(
    result: Result = Depends(get_result_from_session),
    questionnaire: Questionnaire = Depends(initialize_questionnaire_from_session),
) -> AnalyticsResponse:
    analytics = questionnaire.get_analytics(result)

    return AnalyticsResponse(analytics=analytics)
