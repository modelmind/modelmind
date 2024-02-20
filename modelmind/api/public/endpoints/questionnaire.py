from fastapi import APIRouter, Depends, Path, Body, HTTPException
from modelmind.api.public.dependencies.session import verify_session_status, create_jwt_session_token, create_session
from modelmind.db.schemas.sessions import DBSession, SessionStatus
from modelmind.commands.next_questions import NextQuestionsCommand, NextQuestions
from modelmind.api.public.dependencies.questionnaire import initialize_questionnaire
from modelmind.api.public.dependencies.results import initialize_results
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
async def next_questions(
    current_result: Result = Depends(initialize_results),
    questionnaire: Questionnaire = Depends(initialize_questionnaire),
) -> NextQuestions:

    try:
        return await NextQuestionsCommand(
            questionnaire=questionnaire,
            current_result=current_result,
        ).run()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
