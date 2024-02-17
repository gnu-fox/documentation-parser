from abc import ABC, abstractmethod
from typing import Union
from typing import Dict, List
from collections import deque

from src.domain.events import Event, Command
from src.services.handlers import Handler
from src.services.repository import Repository

class Messagebus:
    def __init__(self, repository : Repository):
        self.repository = repository
        self.queue = deque()
        self.publishers : Dict[str, Handler[Command]] = {}
        self.consumers : Dict[str, List[Handler[Event]]] = {}

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
                self.queue.extend(self.repository.events)
            except Exception:
                print(f"Exception handling event {event}")
                continue

    async def publish(self, command: Command):
        print(f"handling command {command}")
        try:
            handler = self.publishers[command.type]
            await handler(command)
            self.queue.extend(self.repository.events)
        except Exception:
            print(f"Exception handling command {command}")
            raise

    async def start(self):
        while True:
            message = self.queue.popleft()
            await self.handle(message)