from modelmind.api.exceptions import ConflictException, GoneException, InternalServerException, NotFoundException


class SessionNotFoundException(NotFoundException):
    def __init__(self, session_id: str):
        detail = f"Session with ID {session_id} not found"
        super().__init__(detail=detail)


class SessionAlreadyCompletedException(ConflictException):
    def __init__(self, session_id: str):
        detail = f"Session with ID {session_id} already completed"
        super().__init__(detail=detail)


class SessionInProgressException(ConflictException):
    def __init__(self, session_id: str):
        detail = f"Session with ID {session_id} not yet completed"
        super().__init__(detail=detail)


class SessionExpiredException(GoneException):
    def __init__(self, session_id: str):
        detail = f"Session with ID {session_id} expired"
        super().__init__(detail=detail)


class UnknownSessionStatusException(InternalServerException):
    def __init__(self, session_id: str | None = None):
        detail = "Unknown session status" if session_id is None else f"Unknown status for session with ID {session_id}"
        super().__init__(detail=detail)
