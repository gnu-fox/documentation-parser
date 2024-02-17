import os
import pytest
import logging

from uuid import uuid4

from src.domain.events import Event, Command
from src.domain.models import Folder, File
from src.domain.models import Project
from src.services.handlers import Handler
from src.services.repository import Repository
from src.services.messagebus import Messagebus

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


class StartProjectProcessing(Handler[Command]):

    def __init__(self, repository : Repository):
        self.repository = repository

    async def __call__(self, command: Command):
        project = self.repository.get(command.payload['project_id'])
        load_from_data_dir(project.root)

        if not project:
            raise Exception(f"Project with id {command.payload['project_id']} not found")
        else:
            print(f"Starting processing of project {project.id}")


        for file in project.files:
            if file.extension == '.md':
                project.events.append(Event(type='readme-detected', payload={'folder': project.root.path}))
                print(f"readme file detected in folder {project.root.path}")
            elif file.extension == '.py':
                with open(file.path, 'r') as f:
                    content = f.read()
                    if 'async def ' in content:
                        project.events.append(Event(type='async-function-detected', payload={'filename': file.name}))
                        print(f"async function detected in file {file.name}")
                    elif 'def ' in content:
                        project.events.append(Event(type='function-detected', payload={'filename': file.name}))
                        print(f"function detected in file {file.name}")
                    elif 'class ' in content:
                        project.events.append(Event(type='class-detected', payload={'filename': file.name}))
                        print(f"class detected in file {file.name}")

class ReadmeFileDetected(Handler[Event]):
    def __init__(self, fake_db_deps):
        pass

    async def __call__(self, event: Event):
        logging.info(f"readme file detected in folder {event.payload['folder']} ")
        logging.info(f"calling the model to process the file")


class FunctionDectected(Handler[Event]):
    def __init__(self, fake_db_deps):
        pass

    async def __call__(self, event: Event):
        logging.info(f"function detected in file {event.payload['filename']} ")
        logging.info(f"calling the model to process it")


class AsyncFunctionDectected(Handler[Event]):
    def __init__(self, fake_db_deps):
        pass

    async def __call__(self, event: Event):
        logging.info(f"async function detected in file {event.payload['filename']} ")
        logging.info(f"calling the model to process it")
        

class ClassDetected(Handler[Event]):
    def __init__(self, fake_db_deps):
        pass

    async def __call__(self, event: Event):
        logging.info(f"class detected in file {event.payload['filename']} ")
        logging.info(f"calling the model to process it")


@pytest.mark.asyncio
async def test_messagebus():
    repository = Repository()

    project_id = uuid4()
    repository.add(Project(id = project_id, root=Folder(path='./', name='root')))

    messagebus = Messagebus(repository)


    messagebus.publishers['start-project-processing'] = StartProjectProcessing(repository)

    messagebus.consumers['readme-detected'] = [ReadmeFileDetected(None)]
    messagebus.consumers['function-detected'] = [FunctionDectected(None)]
    messagebus.consumers['async-function-detected'] = [AsyncFunctionDectected(None)]
    messagebus.consumers['class-detected'] = [ClassDetected(None)]


    await messagebus.handle(Command(type='start-project-processing', payload={'project_id': project_id}))

