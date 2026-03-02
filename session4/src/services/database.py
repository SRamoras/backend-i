# import json
# from pathlib import Path
# from data.models import Meeting
# from uuid import uuid4

# BASE_PATH = Path("meetings") 
# INDEX_PATH = Path("meeting/index.json")
    
# def create(meeting:Meeting):
#     filename = f"{BASE_PATH}/{uuid4()}.md"
#     breakpoint()
#     with open(filename, "w") as file:
#         file.writelines(str(meeting))

#     if not INDEX_PATH.exists():
#         INDEX_PATH.touch()

#     index_content = None
    
#     with open(INDEX_PATH.absolute(),"r") as file:
#         index_content = json.loads(file.read())
#         print(index_content)









from data.models import Meeting
from uuid import uuid4

BASE_PATH = "meetings"

def create(meeting: Meeting):
    id = uuid4()
    fileName = f"{BASE_PATH}/{id}.md"
    fileJson = f"storage.json"

    with open(fileName, "w") as file:
        file.writelines(str(meeting))

    with open(fileJson,'r') as file:
        content = file.read()

    with open(fileJson, "w") as file:
        file.writelines(f"""{content[:1]}
{{"path": "{fileName}",
"title": "{meeting.title}",
"owner": "{meeting.owner}",
"date": "{meeting.date}"
}}{content[1:]}
""")    