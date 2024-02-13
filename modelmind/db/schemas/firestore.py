from pydantic import BaseModel


class Document(BaseModel):
    ...


class DocumentCreate(Document):
    pass
