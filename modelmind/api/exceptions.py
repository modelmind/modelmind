from fastapi import HTTPException


class BadRequestException(HTTPException):
    def __init__(self, detail):
        super().__init__(status_code=400, detail=detail)


class UnauthorizedException(HTTPException):
    def __init__(self, detail):
        super().__init__(status_code=401, detail=detail)


class UnsupportedMediaTypeException(HTTPException):
    def __init__(self, detail):
        super().__init__(status_code=415, detail=detail)


class ForbiddenException(HTTPException):
    def __init__(self, detail):
        super().__init__(status_code=403, detail=detail)


class NotFoundException(HTTPException):
    def __init__(self, detail):
        super().__init__(status_code=404, detail=detail)


class ConflictException(HTTPException):
    def __init__(self, detail):
        super().__init__(status_code=409, detail=detail)


class GoneException(HTTPException):
    def __init__(self, detail):
        super().__init__(status_code=410, detail=detail)


class TooManyRequestsException(HTTPException):
    def __init__(self, detail):
        super().__init__(status_code=429, detail=detail)


class InternalServerException(HTTPException):
    def __init__(self, detail):
        super().__init__(status_code=500, detail=detail)
