from abc import ABC, abstractmethod
from typing import Generic
from typing import TypeVar
from pydantic import BaseModel

Input = TypeVar("Input", bound=BaseModel)
Output = TypeVar("Output", bound=BaseModel)


class Command(Generic[Input, Output], ABC):
    def __init__(self, params: Input):
        self.params: Input = params

    async def run(self) -> Output:
        output = await self._run()
        await self.after_run_completed(output)
        return output

    @abstractmethod
    async def _run(self) -> Output:
        # This method should be overridden by subclasses to implement specific logic
        ...

    async def after_run_completed(self, output: Output) -> None:
        ...


__all__ = ["Command"]
