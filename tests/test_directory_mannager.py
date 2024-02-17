import os
import pytest
import logging
import asyncio

from uuid import uuid4

from src.model.events import Event, Command
from src.model.models import Folder, File
from src.model.messagebus import Handler, DirectoryManager

SUPPORTED_EXTENSIONS = ['.py', '.md']
CREATED_EVENTS = []

def load_from_data_dir(folder : Folder):
    items = os.listdir(folder.path)
    for item in items:
        path = os.path.join(folder.path, item)

        if os.path.isdir(path):
            child = Folder(name = item, path = path)
            folder.children.append(child)
            load_from_data_dir(child)

        elif os.path.isfile(path):
            name, extension = os.path.splitext(item)
            if extension in SUPPORTED_EXTENSIONS:
                with open(path, 'r') as file:
                    content = file.read()
                child = File(name = name, path = path, extension = extension, content = content)
                folder.children.append(child)


class StartFileProcessing(Handler[Command]):

    def __init__(self, folder : Folder):
        self.folder = folder

    async def __call__(self, command: Command):
        logging.info(f"Starting processing of folder {command.payload['path']}")
        load_from_data_dir(self.folder)
        await asyncio.sleep(1)    

        for file in self.folder.files:
            if file.extension == '.md':
                file.events.append(Event(type='readme-detected', payload={'path' : file.path}))
                logging.info(f"readme file detected {file.path}")

            elif file.extension == '.py':
                with open(file.path, 'r') as f:
                    content = f.read()
                    if 'async def ' in content:
                        file.events.append(Event(type='async-function-detected', payload={'filename': file.name}))
                        logging.info(f"async function detected in file {file.name}")
                    elif 'def ' in content:
                        file.events.append(Event(type='function-detected', payload={'filename': file.name}))
                        logging.info(f"function detected in file {file.name}")
                    elif 'class ' in content:
                        file.events.append(Event(type='class-detected', payload={'filename': file.name}))
                        logging.info(f"class detected in file {file.name}")


class ReadmeFileDetected(Handler[Event]):
    def __init__(self, folder : Folder):
        self.folder = folder

    async def __call__(self, event: Event):
        print(f"readme file detected {event.payload['filename']} ")
        print(f"calling the model to process the file")
        await asyncio.sleep(3)    


class FunctionDectected(Handler[Event]):
    def __init__(self, fake_db_deps):
        pass

    async def __call__(self, event: Event):
        print(f"function detected in file {event.payload['filename']} ")
        print(f"calling the model to process it")
        await asyncio.sleep(3)    


class AsyncFunctionDectected(Handler[Event]):
    def __init__(self, fake_db_deps):
        pass

    async def __call__(self, event: Event):
        print(f"async function detected in file {event.payload['filename']} ")
        print(f"calling the model to process it")
        await asyncio.sleep(3)    
        

class ClassDetected(Handler[Event]):
    def __init__(self, fake_db_deps):
        pass

    async def __call__(self, event: Event):
        print(f"class detected in file {event.payload['filename']} ")
        print(f"calling the model to process it")
        await asyncio.sleep(3)    


@pytest.mark.asyncio
async def test_messagebus():
    root=Folder(path='./', name='root')
    messagebus = DirectoryManager(root)
    messagebus.publishers['start-file-processing'] = StartFileProcessing(root)
    messagebus.consumers['readme-detected'] = [ReadmeFileDetected(None)]
    messagebus.consumers['function-detected'] = [FunctionDectected(None)]
    messagebus.consumers['async-function-detected'] = [AsyncFunctionDectected(None)]
    messagebus.consumers['class-detected'] = [ClassDetected(None)]
    await messagebus.handle(Command(type='start-file-processing', payload={'path': './'}))

