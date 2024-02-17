import os

from domain.models import Folder
from domain.models import File
from domain.models import Project

#mock adapter for development

SUPPORTED_EXTENSIONS = ['.py']

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

def mock_project() -> Project:
    project = Project(path = './')
    load_from_data_dir(project.root)
    return project