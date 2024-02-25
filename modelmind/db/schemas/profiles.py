from typing import List
from uuid import uuid4

from pydantic import Field

from . import DBIdentifier, DBIdentifierUUID, DBObject, DBObjectCreate


class CreateProfile(DBObjectCreate):
    id: DBIdentifierUUID = Field(default_factory=uuid4)


class DBProfile(DBObject):
    sessions: List[DBIdentifier] = []
    results: List[DBIdentifier] = []
