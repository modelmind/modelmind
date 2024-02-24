from typing import List

from fastapi import Depends, HTTPException, Path

from modelmind.api.public.dependencies.session.get import get_session_from_token
from modelmind.community.engines.engine_factory import EngineFactory
from modelmind.db.daos.questionnaires import QuestionnairesDAO
from modelmind.db.exceptions.questionnaires import QuestionnaireNotFound
from modelmind.db.schemas.questionnaires import DBQuestionnaire
from modelmind.db.schemas.questions import DBQuestion
from modelmind.db.schemas.sessions import DBSession
from modelmind.models.questionnaires.base import Questionnaire
from modelmind.models.questions.base import Question


async def get_questionnaire_by_name(name: str = Path(...)) -> DBQuestionnaire:
    try:
        # TODO: Cache this
        return await QuestionnairesDAO.get_from_name(name)
    except QuestionnaireNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def validate_requested_language(
    questionnaire: DBQuestionnaire = Depends(get_questionnaire_by_name),
    language: str = Path(..., description="The language code for the questionnaire"),
) -> str:
    # TODO: we may want to check the languages available for the questions given a questionnaire name
    available_languages = ["en"]

    if language not in available_languages:
        raise HTTPException(status_code=400, detail=f"Language {language} not available for this questionnaire")
    return language


async def get_questionnaire_from_session(session: DBSession = Depends(get_session_from_token)) -> DBQuestionnaire:
    try:
        # TODO: Cache this
        return await QuestionnairesDAO.get_from_id(session.questionnaire_id)
    except QuestionnaireNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_language_from_session(session: DBSession = Depends(get_session_from_token)) -> str:
    return session.language


async def get_questions_from_session(
    questionnaire: DBQuestionnaire = Depends(get_questionnaire_from_session),
    language: str = Depends(get_language_from_session),
) -> List[DBQuestion]:
    try:
        # TODO: Cache this
        return await QuestionnairesDAO.get_questions(questionnaire.id, language)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch questions: {str(e)}")


async def initialize_questionnaire_from_session(
    db_questionnaire: DBQuestionnaire = Depends(get_questionnaire_from_session),
    db_questions: List[DBQuestion] = Depends(get_questions_from_session),
) -> Questionnaire:
    # TODO: Convert the DBQuestion models to the correct BaseQuestion models
    # BaseQuestion is abstract, so we need to convert to the correct subclass
    questions = [Question(**question.model_dump()) for question in db_questions]

    engine = EngineFactory.get_engine(db_questionnaire.engine)(questions)

    return Questionnaire(name=db_questionnaire.name, engine=engine, questions=questions)
