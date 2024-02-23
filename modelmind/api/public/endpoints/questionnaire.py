from fastapi import APIRouter, Depends, Path, Body, HTTPException
from modelmind.api.public.dependencies.session import verify_session_status, create_jwt_session_token, create_session
from modelmind.db.schemas.sessions import DBSession, SessionStatus
from modelmind.db.daos.results import ResultsDAO
from modelmind.api.public.dependencies.questionnaire import initialize_questionnaire
from modelmind.api.public.dependencies.results import get_results
from modelmind.api.public.dependencies.daos import results_dao_provider
from modelmind.api.public.schemas.next_questions import NextQuestions
from modelmind.api.public.schemas.analytics import Analytics
from modelmind.models.questionnaires.base import Questionnaire
from modelmind.models.questions.base import BaseQuestion
from modelmind.models.results.base import Result

router = APIRouter(prefix="/questionnaire")


@router.get("/{name}/{language}/session")
async def start_questionnaire_session(
    name: str = Path(..., description="The ID of the questionnaire"),
    language: str = Path(..., description="The language code for the questionnaire")
) -> dict:
    session_id = await create_session(name, language, {})
    session_token = create_jwt_session_token(session_id)
    return {"x-session-token": session_token}


@router.post("/{name}/questions/{language}/next", response_model=NextQuestions, dependencies=[Depends(verify_session_status)])
async def next(
    current_result: Result = Depends(get_results),
    questionnaire: Questionnaire = Depends(initialize_questionnaire),
    results_dao: ResultsDAO = Depends(results_dao_provider),
) -> NextQuestions:

    if questionnaire.is_completed(current_result):
        raise HTTPException(status_code=400, detail="Questionnaire already completed")

    next_questions = await questionnaire.next_questions(current_result)
    analytics = questionnaire.get_analytics(current_result)

    return NextQuestions(
        questions=next_questions,
        analytics=analytics,
        session_status=SessionStatus.IN_PROGRESS
    )

    # Check if the questionnaire is completed
    #if questionnaire completed then save to DB + return empty list

    # if not completed, then get next questions
