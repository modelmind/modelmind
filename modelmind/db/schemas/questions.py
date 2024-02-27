from pydantic import BaseModel, ConfigDict


class DBQuestion(BaseModel):
    language: str

    model_config = ConfigDict(extra="allow")
