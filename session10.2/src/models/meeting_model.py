from datetime import datetime
from uuid import UUID

class Meeting:
    id:UUID
    name:str
    owner:str
    date:datetime