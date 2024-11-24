import asyncio

from fastapi import APIRouter, Depends, Response

from modelmind.api._dependencies.daos.providers import (
    profiles_dao_provider,
    results_dao_provider,
    sessions_dao_provider,
)
from modelmind.api._dependencies.notifier import get_event_notifier
from modelmind.api._dependencies.profile import get_or_create_profile
from modelmind.api._dependencies.questionnaire import (
    get_language_from_path,
    get_questionnaire_by_id,
    initialize_questionnaire_from_id,
    initialize_questionnaire_from_session,
)
from modelmind.api._dependencies.results import get_result, get_result_from_session
from modelmind.api._dependencies.session.create import create_jwt_session_token, create_session
from modelmind.api._dependencies.session.get import get_session_from_token
from modelmind.api._dependencies.session.verify import session_status_completed, session_status_in_progress
from modelmind.api.business.analytics.schemas import AnalyticsResponse
from modelmind.api.business.profiles.schemas import SessionResponse
from modelmind.api.business.questionnaires.schemas import NextQuestionsResponse
from modelmind.api.business.results.schemas import ResultsResponse, ResultVisibility
from modelmind.commands.send_result_notification import SendResultNotificationCommand
from modelmind.config import settings
from modelmind.db.daos.profiles import ProfilesDAO
from modelmind.db.daos.results import ResultsDAO
from modelmind.db.daos.sessions import SessionsDAO
from modelmind.db.schemas.profiles import DBProfile
from modelmind.db.schemas.questionnaires import DBQuestionnaire
from modelmind.db.schemas.results import DBResult
from modelmind.db.schemas.sessions import DBSession
from modelmind.models.questionnaires.base import Questionnaire
from modelmind.models.results.base import Result
from modelmind.services.event_notifier import EventNotifier

router = APIRouter(prefix="/questionnaire")


@router.get("/{id}/{language}/session", operation_id="start_questionnaire_session")
async def questionnaire_session_start(
    response: Response,
    language: str = Depends(get_language_from_path),
    questionnaire: DBQuestionnaire = Depends(get_questionnaire_by_id),
    profile: DBProfile = Depends(get_or_create_profile),
    profiles_dao: ProfilesDAO = Depends(profiles_dao_provider),
    sessions_dao: SessionsDAO = Depends(sessions_dao_provider),
) -> SessionResponse:
    session = await create_session(profile.id, questionnaire.id, language, {}, sessions_dao)
    await profiles_dao.add_session(profile.id, session.id)
    session_token = create_jwt_session_token(session.id, profile.id)
    response.set_cookie(
        key=settings.mm_session_cookie,
        value=session_token,
        domain=settings.domain,
        httponly=True,
        secure=True,
        samesite="strict",
    )
    return SessionResponse(
        profile_id=str(profile.id),
        session_id=str(session.id),
        questionnaire_id=str(questionnaire.id),
        status=session.status.value,
        language=session.language,
        expires_at=session.expires_at,
    )


@router.post(
    "/session/questions/next",
    response_model=NextQuestionsResponse,
    dependencies=[Depends(session_status_in_progress)],
    operation_id="get_questionnaire_session_next_questions",
)
async def questionnaire_session_questions_next(
    current_result: Result = Depends(get_result),
    questionnaire: Questionnaire = Depends(initialize_questionnaire_from_session),
    session: DBSession = Depends(get_session_from_token),
    sessions_dao: SessionsDAO = Depends(sessions_dao_provider),
    results_dao: ResultsDAO = Depends(results_dao_provider),
    profiles_dao: ProfilesDAO = Depends(profiles_dao_provider),
    notifier: EventNotifier = Depends(get_event_notifier),
) -> NextQuestionsResponse:
    """Get the next questions for the current session and result"""

    if questionnaire.is_completed(current_result):
        current_result.label = questionnaire.get_result_label(current_result)
        db_result = await results_dao.create(
            session_id=session.id,
            questionnaire_id=session.questionnaire_id,
            profile_id=session.profile_id,
            data=current_result.data,
            label=current_result.label,
            language=session.language,
        )
        await profiles_dao.add_result(session.profile_id, db_result.id)
        await sessions_dao.set_result(session.id, db_result.id)

        send_result_notifcation = SendResultNotificationCommand(
            questionnaire, current_result, notifier, session.profile_id, profiles_dao
        )
        asyncio.create_task(send_result_notifcation.run())

        return NextQuestionsResponse(
            questions=[], completed=current_result.answered_questions_count(), remaining=0, result_id=str(db_result.id)
        )

    next_questions = await questionnaire.next_questions(current_result)
    remaining = await questionnaire.get_remaining_questions_count(current_result)
    completed = current_result.answered_questions_count()

    return NextQuestionsResponse(questions=next_questions, completed=completed, remaining=remaining)


@router.get(
    "/session/results",
    response_model=ResultsResponse,
    dependencies=[Depends(session_status_completed)],
    operation_id="get_questionnaire_session_results",
)
async def questionnaire_session_results(
    db_result: DBResult = Depends(get_result_from_session),
) -> ResultsResponse:
    return ResultsResponse(
        id=str(db_result.id),
        profile_id=str(db_result.profile_id),
        questionnaire_id=str(db_result.questionnaire_id),
        session_id=str(db_result.session_id),
        data=db_result.data,
        created_at=db_result.created_at,
        visibility=ResultVisibility(db_result.visibility),
        label=db_result.label,
        language=db_result.language,
    )


@router.get("/session", response_model=SessionResponse, operation_id="get_current_session")
async def get_current_session(
    session: DBSession = Depends(get_session_from_token),
) -> SessionResponse:
    return SessionResponse(
        profile_id=str(session.profile_id),
        session_id=str(session.id),
        result_id=str(session.result_id) if session.result_id else None,
        questionnaire_id=str(session.questionnaire_id),
        status=session.status.value,
        language=session.language,
        expires_at=session.expires_at,
    )


@router.put("/session/language", operation_id="update_current_session_language")
async def update_current_session_language(
    session: DBSession = Depends(get_session_from_token),
    sessions_dao: SessionsDAO = Depends(sessions_dao_provider),
) -> None:
    await sessions_dao.update_language(session.id, session.language)


@router.post(
    "/{id}/{language}/analytics",
    response_model=AnalyticsResponse,
    operation_id="calculate_questionnaire_result_analytics",
)
async def calculate_questionnaire_result_analytics(
    result: Result = Depends(get_result),
    questionnaire: Questionnaire = Depends(initialize_questionnaire_from_id),
) -> AnalyticsResponse:
    analytics = questionnaire.get_analytics(result)

    return AnalyticsResponse(analytics=analytics)
