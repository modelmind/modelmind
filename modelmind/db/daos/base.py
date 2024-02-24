from abc import ABC
from typing import Any, AsyncIterable, Dict, Generic, List, Optional, Type, TypeVar

from db.exceptions.base import DBObjectNotFound
from db.firestore import firestore_client as db
from db.schemas import DBIdentifier
from db.utils.type_adapter import TypeAdapter
from google.cloud.firestore import AsyncCollectionReference, DocumentReference, DocumentSnapshot
from pydantic import BaseModel

# Generic type for documents stored in Firestore
T = TypeVar("T", bound=BaseModel)


class FirestoreDAO(Generic[T], ABC):
    _collection_name: str = ""
    # Specify the type of the Pydantic model for deserialization
    model: Type[T]

    @classmethod
    def db(cls) -> AsyncIterable:
        """Get a reference to the Firestore database."""
        return db

    @classmethod
    def collection_name(cls) -> str:
        """
        Determine the collection name. Use the class name if _collection_name is not explicitly set.
        """
        if not cls._collection_name:
            return cls.__name__.split("DAO")[0].lower()
        return cls._collection_name

    @classmethod
    def collection(cls) -> AsyncCollectionReference:
        """Get a reference to the Firestore collection."""
        return db.collection(cls.collection_name())

    @classmethod
    async def get(cls, document_id: DBIdentifier) -> T:
        """Fetch a single document and parse it into the model."""
        doc_ref: DocumentReference = cls.collection().document(document_id)
        doc: DocumentSnapshot = await doc_ref.get()
        if not doc.exists:
            raise DBObjectNotFound(f"Document with ID {document_id} not found in {cls.collection_name}.")
        return cls.model.model_validate(doc.to_dict())

    @classmethod
    async def add(cls, document_data: Dict[str, Any]) -> T:
        """Add a new document to the collection."""
        doc_ref: DocumentReference = cls.collection().document()
        await doc_ref.set(document_data)
        return cls.model.model_validate(document_data)

    @classmethod
    async def update(cls, document_id: DBIdentifier, data: Dict[str, Any]) -> None:
        """Update an existing document."""
        doc_ref: DocumentReference = cls.collection().document(document_id)
        await doc_ref.update(data)

    @classmethod
    async def delete(cls, document_id: DBIdentifier) -> None:
        """Delete a document from the collection."""
        await cls.collection().document(document_id).delete()

    @classmethod
    async def query(cls, query_params: List) -> List[T]:
        """Query the collection based on provided parameters."""
        query: AsyncCollectionReference = cls.collection()
        for param in query_params:
            query = query.where(*param)
        docs: list[DocumentSnapshot] = await query.get()
        return TypeAdapter.validate(List[T], [doc.to_dict() for doc in docs])
