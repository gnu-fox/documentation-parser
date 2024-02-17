from uuid import uuid4
from uuid import UUID
from typing import Any
from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

class Message(BaseModel):
    id : UUID = Field(default_factory=uuid4)
    timestamp : datetime = Field(default_factory=datetime.now)
    model_config = ConfigDict(frozen=True)

class Event(Message):
    type : str = Field(..., alias="type", description="The type of the Event")
    payload : Any

class Command(Message):
    type : str = Field(..., alias="type", description="The type of the Command")
    payload : Any