from uuid import UUID
from uuid import uuid4
from datetime import datetime
from typing import Union
from typing import List
from typing import Deque
from typing import Generator
from collections import deque

from pydantic import BaseModel
from pydantic import Field
from pydantic import ConfigDict
from pydantic.dataclasses import dataclass
from pydantic_settings import BaseSettings

from src.model.events import Event

class Content(BaseModel):
    raw : str

@dataclass
class File:
    path : str
    name : str
    extension : str
    content : Union[str, Content]
    events : Deque[Event] = deque()

    def collect_events(self) -> Generator[Event, None, None]:
        while self.events:
            yield self.events.popleft()

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, File):
            return self.path == __value.path
        return False
    
    def __hash__(self) -> int:
        return hash(self.path)


class Folder:
    def __init__(self, path : str, name : str):
        self.path = path
        self.name = name
        self.children : List[Union[Folder, File]] = []
        self.collection = set(self.files)

    @property
    def files(self) -> Generator[File, None, None]:
        for child in self.children:
            if isinstance(child, Folder):
                for file in child.files:
                    yield file
            elif isinstance(child, File):
                yield child

    def get(self, path : str):
        for child in self.children:
            if child.path == path:
                return child
            elif isinstance(child, Folder):
                return child.get(path)
        return None

    def collect_events(self) -> Generator[Event, None, None]:
        for file in self.collection:
            yield from file.collect_events()

    def print(self, indent=''):
        for child in self.children:
            if isinstance(child, Folder):
                if any(isinstance(child, File) for child in self.children):
                    print(indent + '├── ' + child.name + ' (Directory)')
                    child.print(indent + '│   ')
            elif isinstance(child, File):
                print(indent + '├── ' + child.name + child.extension + ' (File)')