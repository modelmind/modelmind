from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

DBIdentifierUUID = UUID
DBIdentifierStr = str

DBIdentifier = DBIdentifierUUID | DBIdentifierStr


class DBObject(BaseModel):
    id: DBIdentifier
    created_at: datetime
    updated_at: datetime


class DBObjectCreate(DBObject):
    id: DBIdentifierUUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class DBOBjectUpdate(DBObject):
    updated_at: datetime = Field(default_factory=datetime.utcnow)
