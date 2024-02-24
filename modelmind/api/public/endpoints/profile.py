from fastapi import APIRouter

router = APIRouter(prefix="/profile")


@router.get("/results/questionnaire/{id}")
async def get_questionnaire_results(id: str) -> list:
    return []


@router.get("/me")
async def get_my_profile() -> dict:
    return {"name": "", "email": "", "phone": ""}
