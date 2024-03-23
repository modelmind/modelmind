from fastapi import APIRouter, Depends

from modelmind.api.public.dependencies.daos.providers import profiles_dao_provider
from modelmind.api.public.dependencies.session.get import get_session_from_token
from modelmind.db.daos.profiles import ProfilesDAO
from modelmind.db.schemas.profiles import Biographics, DBProfile
from modelmind.db.schemas.sessions import DBSession

router = APIRouter(prefix="/profile")


@router.put("/me/biographics")
async def update_profile_biographics(
    biographics: Biographics,
    session: DBSession = Depends(get_session_from_token),
    profiles_dao: ProfilesDAO = Depends(profiles_dao_provider),
) -> None:
    return await profiles_dao.update_biographics(profile_id=session.profile_id, biographics=biographics)


@router.get("/me")
async def get_my_profile(
    session: DBSession = Depends(get_session_from_token),
    profiles_dao: ProfilesDAO = Depends(profiles_dao_provider),
) -> DBProfile:
    return await profiles_dao.get_from_id(session.profile_id)
