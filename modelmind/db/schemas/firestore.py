from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID, uuid4



class Document(BaseModel):
    uuid: UUID
    created_at: datetime
    updated_at: datetime


class DocumentCreate(Document):
    uuid: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class DocumentUpdate(Document):
    updated_at: datetime = Field(default_factory=datetime.utcnow)
