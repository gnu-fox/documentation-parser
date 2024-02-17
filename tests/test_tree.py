import pytest
import os
import logging
from uuid import uuid4

from src.model.models import Folder
from src.model.models import File

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



def test_mock_project():
    logging.basicConfig(level=logging.INFO)
    root=Folder(path='./', name='root')
    load_from_data_dir(root)
    

    for file in root.files:
        assert file.extension in SUPPORTED_EXTENSIONS
        logging.info(f"Loaded file: {file.name}")

    print("Project structure of the current project:")
    root.print()