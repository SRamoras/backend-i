from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

class Meeting(BaseModel):
    id:UUID
    name:str
    owner:str
    date:datetime
