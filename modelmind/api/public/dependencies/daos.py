from modelmind.db.daos.results import ResultsDAO
from modelmind.db.daos.questionnaires import QuestionnairesDAO
from modelmind.db.daos.sessions import SessionsDAO
from modelmind.db.daos.profiles import ProfilesDAO

def results_dao_provider() -> ResultsDAO:
    return ResultsDAO()

def questionnaires_dao_provider() -> QuestionnairesDAO:
    return QuestionnairesDAO()

def sessions_dao_provider() -> SessionsDAO:
    return SessionsDAO()

def profiles_dao_provider() -> ProfilesDAO:
    return ProfilesDAO()
