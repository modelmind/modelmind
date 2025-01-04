import abc

import modelmind.repository as repository


class AbstractUnitOfWork(abc.ABC):
    batches: repository.AbstractRepository  # (1)

    def __init__(self, messagebus):
        self.messagebus = messagebus

    def __enter__(self):  # (2)
        return self

    def __exit__(self, *args):  # (2)
        self.rollback()  # (4)

    def commit(self):
        self._commit()  # (1)
        self.publish_events()  # (2)

    def publish_events(self):  # (2)
        pass

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):  # (4)
        raise NotImplementedError
