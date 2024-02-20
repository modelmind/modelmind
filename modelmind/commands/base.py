from abc import ABC, abstractmethod
from typing import Generic
from typing import TypeVar

Output = TypeVar("Output")


class Command(Generic[Output], ABC):

    def __init__(self) -> None:
        ...

    async def run(self) -> Output:
        await self.before_run()
        output = await self._run()
        await self.after_run(output)
        return output

    async def before_run(self) -> None:
        ...

    @abstractmethod
    async def _run(self) -> Output:
        # This method should be overridden by subclasses to implement specific logic
        ...

    async def after_run(self, output: Output) -> None:
        ...


__all__ = ["Command"]
