from typing import Literal, Optional, Union

from pydantic import BaseModel, Field


class Analytics(BaseModel):
    # TODO: Add support for more item types
    # TODO: may change extra to a more specific type
    class ScoreItem(BaseModel):
        type: Literal["score"] = "score"
        name: str
        value: int | float
        percentage: Optional[float] = None
        categories: list[str] = []

    name: str
    items: list[Union[ScoreItem]] = Field(..., discriminator="type")
    extra: dict

    @property
    def categories(self) -> list[str]:
        return list(set([category for item in self.items for category in item.categories]))
