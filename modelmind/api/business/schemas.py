from abc import ABC

from pydantic import BaseModel


class BaseResponse(BaseModel, ABC):
    pass
