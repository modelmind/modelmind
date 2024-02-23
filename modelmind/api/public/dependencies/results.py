from modelmind.models.results.base import Result
from fastapi import Body, HTTPException


def get_results(data: dict = Body(..., description="The current results of the questionnaire")) -> Result:
    try:
        return Result(data=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


