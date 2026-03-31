import requests
from models.meeting_model import Meeting
def generate_summary(meeting: Meeting):

    prompt = f"""
    Summarize this meeting in bullet points.
    name: {meeting.name}, date: {meeting.date}
    Meeting notes: {meeting.notes}"""

    response = requests.post(
        "http://ollama:11434/api/generate",
        json={
            "model": "phi3",
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()

    return data["response"]