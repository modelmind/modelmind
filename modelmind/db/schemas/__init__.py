from abc import ABC
from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

DBIdentifierUUID = UUID
DBIdentifierStr = str


DBIdentifier = DBIdentifierUUID | DBIdentifierStr


class DBObject(BaseModel, ABC):
    @classmethod
    def id_name(self) -> str:
        return "id"

    id: DBIdentifier
    created_at: datetime
    updated_at: datetime


class DBObjectCreate(BaseModel):
    id: DBIdentifier = Field(default_factory=lambda: str(uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class DBOBjectUpdate(BaseModel):
    updated_at: datetime = Field(default_factory=datetime.utcnow)
