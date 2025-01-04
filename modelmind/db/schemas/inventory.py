from typing import Literal

from typing_extensions import TypedDict


class DBInventory(TypedDict):
    title: str
    description: str
    created_by: str
    settings: dict
    version: int
    status: Literal["draft", "published", "archived"]
    visibility: Literal["public", "private"]
