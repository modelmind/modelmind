from fastapi import Depends
from google.cloud.firestore import AsyncClient

from modelmind.api._dependencies.clients.firestore import get_firestore_client
from modelmind.db.daos.profiles import ProfilesDAO
from modelmind.db.daos.questionnaires import QuestionnairesDAO
from modelmind.db.daos.results import ResultsDAO
from modelmind.db.daos.sessions import SessionsDAO


def results_dao_provider(firestore_client: AsyncClient = Depends(get_firestore_client)) -> ResultsDAO:
    return ResultsDAO(firestore_client)


def questionnaires_dao_provider(firestore_client: AsyncClient = Depends(get_firestore_client)) -> QuestionnairesDAO:
    return QuestionnairesDAO(firestore_client)


def sessions_dao_provider(firestore_client: AsyncClient = Depends(get_firestore_client)) -> SessionsDAO:
    return SessionsDAO(firestore_client)


def profiles_dao_provider(firestore_client: AsyncClient = Depends(get_firestore_client)) -> ProfilesDAO:
    return ProfilesDAO(firestore_client)
