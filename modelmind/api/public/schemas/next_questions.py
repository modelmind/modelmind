from pydantic import BaseModel
from .analytics import Analytics


class NextQuestions(BaseModel):
    questions: list[dict]
    analytics: Analytics

    session_id: str
