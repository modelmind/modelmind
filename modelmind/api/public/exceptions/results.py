from modelmind.api.exceptions import NotFoundException
from modelmind.logger import log


class ResultAccessForbiddenException(NotFoundException):
    def __init__(self, profile_id: str | None, result_id: str):
        log.warning("Profile with ID %s does not have access to result with ID %s", profile_id, result_id)
        detail = f"Profile with ID {profile_id} does not have access to result with ID {result_id}"
        super().__init__(detail=detail)
