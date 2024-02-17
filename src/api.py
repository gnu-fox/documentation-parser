from fastapi import FastAPI
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException, status

from src.services.settings import Settings

async def github_repository(url : str):
    return { 'url': url }

class Documentation:
    def __init__(self, settings : Settings):
        self.settings = settings
        self.router = APIRouter(prefix='/documentation')

    async def generate_documentation(self, repository = Depends(github_repository)):
        pass
        