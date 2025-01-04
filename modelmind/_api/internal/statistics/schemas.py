from pydantic import BaseModel


class CalculateStatisticsRequest(BaseModel):
    questionnaire_id: str
