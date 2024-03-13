from modelmind.models.results.base import Result


class EventNotifier:
    def __init__(self) -> None:
        pass

    async def new_result(self, result: Result) -> None:
        pass
