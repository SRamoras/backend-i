from data.models import Meeting
from uuid import uuid4


BASE_PATH = "meetings"

def create(meeting: Meeting):
    fileName = f"{BASE_PATH}/{uuid4()}.md"
    with open(fileName, "w") as file:
        file.writelines(str(meeting))