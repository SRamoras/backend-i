
from data.models import Meeting, MeetingData
from uuid import uuid4
from pathlib import Path
from dataclasses import asdict
import json

BASE_PATH = Path("meetings") 
INDEX_PATH = Path("meetings/index.json")

def create(meeting: Meeting):
    id = uuid4()
    fileName = f"{BASE_PATH}/{id}.md"

    with open(fileName, "w") as file:
        file.writelines(str(meeting))


    if not INDEX_PATH.exists():
        INDEX_PATH.touch()

    with open(INDEX_PATH,"r") as file:
        if INDEX_PATH.stat().st_size > 0:
            index_content:list = json.load(file)
        else:
            index_content = []
    
    new_index_entry = (
        asdict(MeetingData(
            metting=meeting,
            path=fileName
        ))
    )

    index_content.append(new_index_entry)

    with open(INDEX_PATH, "w") as file:
        json.dump(index_content, file, indent=4)