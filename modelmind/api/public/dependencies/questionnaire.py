import logging
from typing import List

from fastapi import Depends, HTTPException, Path

from modelmind.api.public.dependencies.daos.providers import questionnaires_dao_provider
from modelmind.api.public.dependencies.session.get import get_session_from_token
from modelmind.api.public.exceptions.questionnaires import QuestionnaireNotFoundException
from modelmind.community.engines.engine_factory import EngineFactory
from modelmind.db.daos.questionnaires import QuestionnairesDAO
from modelmind.db.exceptions.questionnaires import DBQuestionnaireNotFound
from modelmind.db.schemas.questionnaires import DBQuestionnaire
from modelmind.db.schemas.questions import DBQuestion
from modelmind.db.schemas.sessions import DBSession
from modelmind.models.questionnaires.base import Questionnaire
from modelmind.models.questions.schemas import Question


async def get_questionnaire_by_name(
    name: str = Path(...), questionnaires_dao: QuestionnairesDAO = Depends(questionnaires_dao_provider)
) -> DBQuestionnaire:
    try:
        # TODO: Cache this
        return await questionnaires_dao.get_from_name(name)
    except DBQuestionnaireNotFound:
        raise QuestionnaireNotFoundException(name)
    except Exception as e:
        logging.error(f"Failed to fetch questionnaire {name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


def validate_requested_language(
    questionnaire: DBQuestionnaire = Depends(get_questionnaire_by_name),
    language: str = Path(..., description="The language code for the questionnaire"),
) -> str:
    # TODO: we may want to check the languages available for the questions in db given a questionnaire name
    available_languages = ["en"]

    if language not in available_languages:
        raise HTTPException(status_code=400, detail=f"Language {language} not available for this questionnaire")
    return language


async def get_questionnaire_from_session(
    session: DBSession = Depends(get_session_from_token),
    questionnaires_dao: QuestionnairesDAO = Depends(questionnaires_dao_provider),
) -> DBQuestionnaire:
    try:
        # TODO: Cache this
        return await questionnaires_dao.get_from_id(session.questionnaire_id)
    except DBQuestionnaireNotFound:
        raise QuestionnaireNotFoundException(str(session.questionnaire_id))
    except Exception as e:
        logging.error(f"Failed to fetch questionnaire {session.questionnaire_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


async def get_language_from_session(session: DBSession = Depends(get_session_from_token)) -> str:
    return session.language


async def get_questions_from_session(
    questionnaire: DBQuestionnaire = Depends(get_questionnaire_from_session),
    questionnaires_dao: QuestionnairesDAO = Depends(questionnaires_dao_provider),
    language: str = Depends(get_language_from_session),
) -> List[DBQuestion]:
    try:
        # TODO: Cache this
        return await questionnaires_dao.get_questions(questionnaire.id, language)
    except Exception as e:
        logging.error(f"Failed to fetch questions for questionnaire {questionnaire.id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch questions: {str(e)}")


async def initialize_questionnaire_from_session(
    db_questionnaire: DBQuestionnaire = Depends(get_questionnaire_from_session),
    db_questions: List[DBQuestion] = Depends(get_questions_from_session),
) -> Questionnaire:
    # TODO: Convert the DBQuestion models to the correct BaseQuestion models
    # BaseQuestion is abstract, so we need to convert to the correct subclass
    questions = [Question(**question.model_dump()) for question in db_questions]

    engine = EngineFactory.create_engine(db_questionnaire.engine, questions=questions, config=None)

    return Questionnaire(name=db_questionnaire.name, engine=engine, questions=questions)
