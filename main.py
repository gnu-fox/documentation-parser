from src.mock_adapter import load_from_data_dir
from src.domain.models import Folder
from src.domain.models import Project

data_folder = './'

project = Project(root = Folder(path='./', name='root'))
load_from_data_dir(project.root)
project.root.print()

for file in project.files:
    print(file.name)
    