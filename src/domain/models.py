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

from src.domain.events import Event

class Content(BaseModel):
    raw : str

class File(BaseModel):
    path : str
    name : str
    extension : str
    content : str

class Folder:
    def __init__(self, path : str, name : str):
        self.path = path
        self.name = name
        self.children : List[Union[Folder, File]] = []

    @property
    def files(self) -> Generator[File, None, None]:
        for child in self.children:
            if isinstance(child, Folder):
                for file in child.files:
                    yield file
            elif isinstance(child, File):
                yield child

    def print(self, indent=''):
        for child in self.children:
            if isinstance(child, Folder):
                if any(isinstance(child, File) for child in self.children):
                    print(indent + '├── ' + child.name + ' (Directory)')
                    child.print(indent + '│   ')
            elif isinstance(child, File):
                print(indent + '├── ' + child.name + child.extension + ' (File)')


class Project:
    def __init__(self, id : UUID, root : Folder):
        self.id = id
        self.root = root
        self.files = self.root.files

        self.events : Deque[Event] = deque()

    