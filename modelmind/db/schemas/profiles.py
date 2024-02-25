from typing import List
from uuid import uuid4

from pydantic import Field

from . import DBIdentifier, DBObject, DBObjectCreate


class CreateProfile(DBObjectCreate):
    id: DBIdentifier = Field(default_factory=lambda: str(uuid4()))


class DBProfile(DBObject):
    sessions: List[DBIdentifier] = []
    results: List[DBIdentifier] = []
