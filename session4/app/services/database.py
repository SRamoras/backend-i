from data.models import Meeting, MeetingData, ActionItem
from uuid import uuid4
from pathlib import Path
from dataclasses import asdict
import json
import csv

BASE_PATH = Path("meetings")
INDEX_PATH = Path("meetings/index.json")


def create(meeting: Meeting):
    BASE_PATH.mkdir(exist_ok=True)
    meeting_id = uuid4()
    file_name = f"{BASE_PATH}/{meeting_id}.md"

    with open(file_name, "w") as file:
        file.writelines(str(meeting))

    if not INDEX_PATH.exists():
        INDEX_PATH.touch()

    with open(INDEX_PATH, "r") as file:
        index_content = json.load(file) if INDEX_PATH.stat().st_size > 0 else []

    index_content.append(asdict(MeetingData(metting=meeting, path=file_name)))

    with open(INDEX_PATH, "w") as file:
        json.dump(index_content, file, indent=4)


def list_meetings() -> list[Meeting]:
    if not INDEX_PATH.exists() or INDEX_PATH.stat().st_size == 0:
        return []

    with open(INDEX_PATH, "r") as file:
        index_content = json.load(file)

    meetings = []
    for entry in index_content:
        m = entry["metting"]
        actions = [ActionItem(**a) for a in m.get("action_items", [])]
        meetings.append(Meeting(
            title=m["title"],
            owner=m["owner"],
            date=m["date"],
            participants=m.get("participants", []),
            action_items=actions
        ))
    return meetings


def export_csv(output_path: str = "meetings/report.csv"):
    meetings = list_meetings()
    with open(output_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["title", "owner", "date", "participants", "total_action_items"])
        for m in meetings:
            writer.writerow([
                m.title,
                m.owner,
                m.date,
                ", ".join(m.participants),
                len(m.action_items)
            ])