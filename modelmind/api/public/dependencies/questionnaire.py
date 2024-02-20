from typing import List
from fastapi import Depends, HTTPException, Path
from modelmind.db.daos.questionnaires import QuestionnairesDAO
from modelmind.db.schemas.questionnaires import DBQuestionnaire
from modelmind.db.schemas.questions import DBQuestion
from modelmind.db.exceptions.questionnaires import QuestionnaireNotFound
from modelmind.models.engines.base import BaseEngine
from modelmind.services.engine_factory import EngineFactory
from modelmind.models.questionnaires.base import Questionnaire
from modelmind.models.questions.base import Question


# TODO: Cache this
async def get_questionnaire_by_name(name: str = Path(...)) -> DBQuestionnaire:
    try:
        return await QuestionnairesDAO.get_by_name(name)
    except QuestionnaireNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# TODO: Cache this
async def get_questions_for_questionnaire(questionnaire: DBQuestionnaire = Depends(get_questionnaire_by_name), language: str = Path(...)) -> List[DBQuestion]:
    try:
        return await QuestionnairesDAO.get_questions(questionnaire.id, language)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch questions: {str(e)}")


async def initialize_questionnaire(
    db_questionnaire: DBQuestionnaire = Depends(get_questionnaire_by_name),
    db_questions: List[DBQuestion] = Depends(get_questions_for_questionnaire),
) -> Questionnaire:

    # TODO: Convert the DBQuestion models to the correct BaseQuestion models
    # BaseQuestion is abstract, so we need to convert to the correct subclass
    questions = [Question(**question.model_dump()) for question in db_questions]

    engine = EngineFactory.get_engine(db_questionnaire.engine)(questions)

    return Questionnaire(name=db_questionnaire.name, engine=engine, questions=questions)

