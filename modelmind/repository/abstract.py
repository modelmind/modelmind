from typing import Any, Generic, Protocol, TypeVar

T = TypeVar("T")


class AbstractRepository(Protocol, Generic[T]):
    """A protocol (interface) for a generic repository with CRUD operations."""

    def __init__(self, **kwargs: Any) -> None: ...

    def add(self, entity: T) -> T:
        """Create a new entity and return it."""
        ...

    def get(self, entity_id: str) -> T | None:
        """Read (retrieve) an entity by its ID. Returns None if not found."""
        ...

    def update(self, entity: T) -> T:
        """Update an existing entity and return the updated entity."""
        ...

    def delete(self, entity_id: str) -> bool:
        """Delete an entity by its ID. Returns True if deletion was successful."""
        ...
