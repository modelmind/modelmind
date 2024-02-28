import logging
from abc import ABC
from time import perf_counter
from typing import Any, AsyncIterator, Dict, Generic, List, Literal, Optional, Type, TypeVar

from google.cloud.firestore import (
    AsyncClient,
    AsyncCollectionReference,
    AsyncDocumentReference,
    DocumentSnapshot,
    FieldFilter,
    Query,
)
from google.cloud.firestore_v1.types import write

from modelmind.db.exceptions.base import DBObjectNotFound
from modelmind.db.firestore import firestore_client as db
from modelmind.db.schemas import DBIdentifier, DBObject

# Generic type for documents stored in Firestore
T = TypeVar("T", bound=DBObject)


class FirestoreDAO(Generic[T], ABC):

    """
    Opiniated base class to manage models persistence in Firestore.

    -> A firestore collection represents a model, and the documents in the collection represent instances of the model.

    # Serialization
    -> Input is not validated to allow more flexibility (partial updates), but should be validated by child class.
    -> Output is always validated to ensure that the document data is consistent with the model.
        -> Schema changes in the firestore document will break the validation
    """

    _collection_name: str = "default"
    # Specify the type of the Pydantic model for deserialization
    model: Type[T]

    @classmethod
    def db(cls) -> AsyncClient:
        """Get a reference to the Firestore database."""
        return db

    @classmethod
    def collection_name(cls) -> str:
        """
        Determine the collection name. Use the class name if _collection_name is not explicitly set.
        """
        if not cls._collection_name:
            return cls.__name__.lower()
        return cls._collection_name

    @classmethod
    def collection(cls) -> AsyncCollectionReference:
        """Get a reference to the Firestore collection."""
        return db.collection(cls._collection_name)

    @classmethod
    def document_ref(cls, document_id: DBIdentifier) -> AsyncDocumentReference:
        """Get a reference to a specific document in the collection."""
        return cls.collection().document(str(document_id))

    @classmethod
    def validate(cls, document_id: DBIdentifier, data: Any) -> T:
        """Validate the input data and return the model."""
        try:
            return cls.model.model_validate({DBObject.id_name(): document_id, **data})
        except Exception as e:
            logging.error(f"Validation failed for document with ID {document_id} in {cls.collection_name()}. {e}")
            raise e

    @classmethod
    async def get(cls, document_id: DBIdentifier) -> T:
        """Fetch a single document and parse it into the model."""
        doc_ref: AsyncDocumentReference = cls.document_ref(document_id)
        doc: DocumentSnapshot = await doc_ref.get()
        if not doc.exists:
            logging.debug(f"Document with ID {document_id} not found in {cls.collection_name()}.")
            raise DBObjectNotFound(f"Document with ID {document_id} not found in {cls.collection_name()}.")
        logging.debug(f"Document with ID {document_id} retrieved from {cls.collection_name()}.")
        return cls.validate(document_id, doc.to_dict())

    @classmethod
    async def add(cls, document_data: Dict[str, Any], document_id: Optional[DBIdentifier] = None) -> T:
        """Add a new document to the collection."""
        document_id = str(document_id) if document_id else document_data.get(DBObject.id_name())
        update_time, doc_ref = await cls.collection().add(document_data, document_id)
        logging.debug(f"Document {doc_ref.id} added to collection {cls.collection_name()} at {update_time}")
        return cls.validate(document_id or doc_ref.id, document_data)

    @classmethod
    async def update(cls, document_id: DBIdentifier, data: Dict[str, Any]) -> None:
        """Update an existing document."""
        doc_ref: AsyncDocumentReference = cls.document_ref(document_id)
        write_result: write.WriteResult = await doc_ref.update(data)
        logging.debug(
            f"Document with ID {document_id} from {cls.collection_name()} updated at {write_result.update_time}"
        )

    @classmethod
    async def delete(cls, document_id: DBIdentifier) -> None:
        """Delete a document from the collection."""
        timestamp = await cls.document_ref(document_id).delete()
        logging.debug(f"Document with ID {document_id} from {cls.collection_name()} deleted at {timestamp}")

    @classmethod
    async def list(
        cls,
        limit: Optional[int] = None,
        order_by: Optional[str] = None,
        direction: Literal["ASCENDING"] | Literal["DESCENDING"] = Query.ASCENDING,
    ) -> List[T]:
        """
        List all documents in the collection.
        """
        query: AsyncCollectionReference = cls.collection()
        if order_by:
            query = query.order_by(order_by, direction=direction)

        if limit:
            query = query.limit(limit)

        docs: AsyncIterator[DocumentSnapshot] = query.stream()

        result: List[T] = []

        start = perf_counter()

        async for doc in docs:
            result.append(cls.validate(doc.id, doc.to_dict()))
            logging.debug(f"Document with ID {doc.id} retrieved from {cls.collection_name()}.")

        logging.info(f"Query took {perf_counter() - start} seconds.")
        return result

    @classmethod
    async def search(
        cls,
        filters: List[FieldFilter],
        limit: Optional[int] = None,
        order_by: Optional[str] = None,
        direction: Literal["ASCENDING"] | Literal["DESCENDING"] = Query.ASCENDING,
    ) -> List[T]:
        """
        Query the collection based on provided parameters.
        """

        query: AsyncCollectionReference = cls.collection()
        for filter in filters:
            query = query.where(filter=filter)

        if order_by:
            query = query.order_by(order_by, direction=direction)

        if limit:
            query = query.limit(limit)

        docs: AsyncIterator[DocumentSnapshot] = query.stream()

        result: List[T] = []

        start = perf_counter()

        async for doc in docs:
            print("doc", doc.id, doc.to_dict())
            result.append(cls.validate(doc.id, doc.to_dict()))
            logging.debug(f"Document with ID {doc.id} retrieved from {cls.collection_name()}.")

        logging.info(f"Query took {perf_counter() - start} seconds.")
        return result

    @classmethod
    async def search_as_dicts(
        cls,
        filters: Optional[List[FieldFilter]] = None,
        limit: Optional[int] = None,
        order_by: Optional[str] = None,
        direction: Literal["ASCENDING"] | Literal["DESCENDING"] = Query.ASCENDING,
    ) -> Dict[DBIdentifier, T]:
        """
        Query the collection based on provided parameters and return as dictionaries with document_id as key.
        """

        query: AsyncCollectionReference = cls.collection()
        if filters:
            for filter in filters:
                query = query.where(filter=filter)

        if order_by:
            query = query.order_by(order_by, direction=direction)

        if limit:
            query = query.limit(limit)

        docs: AsyncIterator[DocumentSnapshot] = query.stream()

        result: Dict[DBIdentifier, T] = {}

        start = perf_counter()

        async for doc in docs:
            result[doc.id] = cls.validate(doc.id, doc.to_dict())
            logging.debug(f"Document with ID {doc.id} retrieved from {cls.collection_name()}.")

        logging.info(f"Query took {perf_counter() - start} seconds.")
        return result

    @classmethod
    async def batch_set(
        cls,
        data: Dict[DBIdentifier, Dict[str, Any]],
        merge: bool = True,
        collection_ref: Optional[AsyncCollectionReference] = None,
    ) -> None:
        """
        Batch set multiple documents in the collection.
        """
        batch = db.batch()
        for doc_id, doc_data in data.items():
            if collection_ref:
                doc_ref = collection_ref.document(doc_id)
            else:
                doc_ref = cls.collection().document(doc_id)
            batch.set(doc_ref, doc_data, merge=merge)

        start = perf_counter()

        write_results: list[write.WriteResult] = await batch.commit()
        logging.info(f"Batch set took {perf_counter() - start} seconds.")

        for i, write_result in enumerate(write_results):
            logging.debug(
                f"Document with ID {write_result.update_time} from {cls.collection_name()}"
                f"updated at {write_result.update_time}"
            )
            if not write_result.update_time:
                raise Exception(f"Document with ID {write_result.update_time} from {cls.collection_name()} not updated")

    @classmethod
    async def batch_add(
        cls, data: List[Dict[str, Any]], collection_ref: Optional[AsyncCollectionReference] = None
    ) -> None:
        """
        Batch add multiple documents to the collection.
        """
        batch = db.batch()
        for doc_data in data:
            if collection_ref:
                doc_ref = collection_ref.document()
            else:
                doc_ref = cls.collection().document()
            batch.set(doc_ref, doc_data)

        start = perf_counter()

        write_results: list[write.WriteResult] = await batch.commit()
        logging.info(f"Batch add took {perf_counter() - start} seconds.")

        for i, write_result in enumerate(write_results):
            logging.debug(
                f"Document with ID {write_result.update_time} from {cls.collection_name()}"
                f"updated at {write_result.update_time}"
            )
            if not write_result.update_time:
                raise Exception(f"Document with ID {write_result.update_time} from {cls.collection_name()} not updated")
