from typing import Optional
from typing import Generator
from typing import Set

from src.domain.events import Event
from src.domain.models import Project

class Repository:
    
    def __init__(self, collection : Set[Project] = set()):
        self.collection : Set[Project] = collection

    def add(self, project : Project):
        self.collection.add(project)
    
    def get(self, id) -> Optional[Project]:
        for project in self.collection:
            if project.id == id:
                return project
        return None

    def remove(self, project : Project):
        self.collection.remove(project)

    @property
    def events(self) -> Generator[Event, None, None]:
        for project in self.collection:
            while project.events:
                yield project.events.popleft()





