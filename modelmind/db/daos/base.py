from abc import ABC, abstractmethod



class FirestoreDAO(ABC):

    @property
    @abstractmethod
    def collection_name(self) -> str:
        pass
