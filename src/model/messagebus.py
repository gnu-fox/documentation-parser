from abc import ABC, abstractmethod
from typing import Union
from typing import TypeVar, Generic
from typing import Dict, List
from collections import deque

from src.model.events import Event, Command
from src.model.models import Folder, File

MSG = TypeVar('MSG', bound=Union[Event, Command])
class Handler(ABC, Generic[MSG]):
    @abstractmethod
    async def __call__(self, message : MSG):
        ...

class MessageBus(ABC):
    def __init__(self):
        self.publishers : Dict[str, Handler[Command]] = {}
        self.consumers : Dict[str, List[Handler[Event]]] = {}
        self.queue = deque()

    @abstractmethod
    def collect_events(self):
        pass

    async def handle(self, message : Union[Event, Command]):
        self.queue.append(message)

        while self.queue:
            message = self.queue.popleft()
            if isinstance(message, Event):
                await self.consume(message)
            elif isinstance(message, Command):
                await self.publish(message)
            else:
                raise Exception(f"{message} was not an Event or Command")

    async def consume(self, event: Event):
        for handler in self.consumers[event.type]:
            try:
                print(f"handling event {event} with handler {handler}")
                await handler(event)
                self.queue.extend(self.collect_events())
            except Exception:
                print(f"Exception handling event {event}")
                continue

    async def publish(self, command: Command):
        print(f"handling command {command}")
        try:
            handler = self.publishers[command.type]
            await handler(command)
            self.queue.extend(self.collect_events())
        except Exception:
            print(f"Exception handling command {command}")
            raise


class FileManager(MessageBus):
    def __init__(self, file : File):
        super().__init__()
        self.file = file
    
    def collect_events(self):
        return self.file.collect_events()
    

class DirectoryManager(MessageBus):
    def __init__(self, root : Folder):
        super().__init__()
        self.root = root

    def collect_events(self):
        return self.root.collect_events()