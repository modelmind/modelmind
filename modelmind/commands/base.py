import abc
import typing

CRT = typing.TypeVar("CRT")


class Command(typing.Generic[CRT], abc.ABC):
    @abc.abstractmethod
    async def _run(self) -> CRT:
        raise NotImplementedError

    async def run(self) -> CRT:
        return await self._run()


__all__ = ["Command"]
