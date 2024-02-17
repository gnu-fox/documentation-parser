from abc import ABC, abstractmethod
from typing import Union
from typing import TypeVar
from typing import Generic

from src.domain.events import Event, Command

MSG = TypeVar('MSG', bound=Union[Event, Command])
class Handler(ABC, Generic[MSG]):
    @abstractmethod
    async def __call__(self, message : MSG):
        ...




