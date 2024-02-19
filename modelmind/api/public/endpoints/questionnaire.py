from fastapi import APIRouter, Depends, Path, Body, HTTPException
from modelmind.api.public.dependencies.session import get_session_from_token, create_jwt_session_token, create_session
from modelmind.db.schemas.sessions import SessionDocument, SessionStatus
from modelmind.commands.next_questions import NextQuestionsParameters, NextQuestionsCommand, NextQuestion


router = APIRouter(prefix="/questionnaire")


@router.get("/{questionnaire_id}/{language}/session")
async def start_questionnaire_session(
    questionnaire_id: str = Path(..., description="The ID of the questionnaire"),
    language: str = Path(..., description="The language code for the questionnaire")
) -> dict:
    # This should return a session token
    session_id = await create_session(questionnaire_id, language, {})
    session_token = create_jwt_session_token(session_id)
    return {"x-session-token": session_token}


@router.post("/{questionnaire_id}/questions/{language}/next", response_model=list[NextQuestion])
async def next_question(
    id: str = Path(..., description="The ID of the questionnaire"),
    language: str = Path(..., description="The language code for the questionnaire"),
    results: dict = Body(..., description="The current results of the questionnaire"),
    session: SessionDocument = Depends(get_session_from_token)
) -> list[NextQuestion]:
    if session.status == SessionStatus.COMPLETED:
        # TODO: change status code
        raise HTTPException(status_code=400, detail="Session already completed")

    params = NextQuestionsParameters(questionnaire_id=id, language=language, results=results)

    try:
        return await NextQuestionsCommand(params).run()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


