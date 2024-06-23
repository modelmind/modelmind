from fastapi import APIRouter, Depends, HTTPException, Path

from modelmind.api.public.dependencies.daos.providers import results_dao_provider
from modelmind.api.public.dependencies.profile import get_profile_optional
from modelmind.api.public.dependencies.results import get_result_from_path, is_result_owner
from modelmind.api.public.schemas.results import ResultsResponse, ResultVisibility
from modelmind.db.daos.results import ResultsDAO
from modelmind.db.schemas.profiles import DBProfile
from modelmind.db.schemas.results import DBResult

router = APIRouter(prefix="/results")


@router.get("/{result_id}", response_model=ResultsResponse)
async def get_public_result(
    db_result: DBResult = Depends(get_result_from_path),
    db_profile: DBProfile | None = Depends(get_profile_optional),
) -> ResultsResponse:
    if db_result.visibility != ResultVisibility.PUBLIC and (
        db_result.id not in db_profile.results if db_profile else True
    ):
        raise HTTPException(status_code=403, detail="Not allowed to access this result")

    return ResultsResponse(
        id=str(db_result.id),
        data=db_result.data,
        created_at=db_result.created_at,
        visibility=ResultVisibility(db_result.visibility),
    )


@router.patch("/{result_id}", dependencies=[Depends(is_result_owner)])
async def update_result_visibility(
    visibility: ResultVisibility,
    result_id: str = Path(..., description="The result id"),
    results_dao: ResultsDAO = Depends(results_dao_provider),
) -> ResultVisibility:
    await results_dao.update_visibility(result_id, DBResult.Visibility(visibility))
    return visibility
