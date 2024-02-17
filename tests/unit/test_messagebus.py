import pytest

from src.domain.models import Event, Content
from src.services.handlers import Handler
from src.services.repository import Repository
from src.services.messagebus import Messagebus

class ReadmeFileDetected(Handler[Event]):
    def __init__(self, fake_db_deps):
        pass

    async def handle(self, event: Event):
        print(f"readme file detected in folder {event.payload['folder']} ")
        print(f"calling the model to process the file")


class FunctionDectected(Handler[Event]):
    def __init__(self, fake_db_deps):
        pass

    async def handle(self, event: Event):
        print(f"function detected in file {event.payload['filename']} ")
        print(f"calling the model to process it")
        

class ClassDetected(Handler[Event]):
    def __init__(self, fake_db_deps):
        pass

    async def handle(self, event: Event):
        print(f"class detected in file {event.payload['filename']} ")
        print(f"calling the model to process it")