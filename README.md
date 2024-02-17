# Document-parser

This package contains the necesary models for parsing documentation concurrently using an async task manager.

### Write your own handlers:

```python
from src.model.models import Folder
from src.model.events import Command
from src.model.messagebus import Handler

class Load(Handler[Command]):

    def __init__(self, folder : Folder):
        self.folder = folder

    async def __call__(self, command: Command):
        logging.info(f"Starting processing of folder {command.payload['path']}")
        load_data_from_dir(self.folder, path = './some/path/with/nested/folders/and/files')

        for file in self.folder:
            file.events.append(Event(type = 'some-event-type', payload = { 'some' : 'payload }))
```

### Inject them into the task mannager and start it:

```python
from src.model.events import Command
from src.model.messagebus import DirectoryManager

async def main():
    root=Folder(path='./', name='root')
    messagebus = DirectoryManager(root)
    messagebus.publishers['load-files'] = Load(root)
    messagebus.consumers['some-events-consumers] = ...
    ...

    await messagebus.handle(Command(type='start-file-processing', payload={'path': './'}))
```

It will automatically start to handle events and commands in parallel thanks to asyncio:


```
14:11:29 [INFO] Starting processing of folder ./
14:11:29 [INFO] function detected in file test_tree
14:11:29 [INFO] async function detected in file test_directory_mannager
14:11:29 [INFO] function detected in file models
14:11:29 [INFO] class detected in file events
14:11:29 [INFO] async function detected in file messagebus
14:11:29 [INFO] readme file detected ./README.md
```

Files also collects events so you can manage them individually using the 'FileManager' class, in for example exposing an api:

```python
from fastapi import FastAPI
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException, status
from fastapi import UploadFile

from src.model.models import File
from src.model.messagebus import FileManager

class DocumentProcessor:
    def __init__(self, prefix = '/doc-processor'):
        self.router = APIRouter(prefix=prefix)
        self.router.add_api_route('/upload', self.upload_file, methods=['POST'])
    
    def mount(self, api : FastAPI):
        api.mount(self.router)

    async def upload_file(self, file: UploadFile):
        ...
```

##TODO list:
* Add infrastructure code
* Add handlers for parsing data
* Add api endpoints
