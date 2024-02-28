from modelmind.api.exceptions import UnauthorizedException


class JWTExpiredException(UnauthorizedException):
    def __init__(self, detail: str = "Token expired"):
        super().__init__(detail=detail)


class JWTInvalidException(UnauthorizedException):
    def __init__(self, detail: str = "Invalid token"):
        super().__init__(detail=detail)


class JWTMissingException(UnauthorizedException):
    def __init__(self, detail: str = "Token missing"):
        super().__init__(detail=detail)
