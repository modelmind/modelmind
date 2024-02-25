from .base import DBOBjectCreationFailed, DBObjectNotFound


class DBProfileNotFound(DBObjectNotFound):
    pass


class DBProfileCreationFailed(DBOBjectCreationFailed):
    pass
