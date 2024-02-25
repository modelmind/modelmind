class DBException(Exception):
    pass


class DBObjectNotFound(DBException):
    pass


class DBOBjectCreationFailed(DBException):
    pass
