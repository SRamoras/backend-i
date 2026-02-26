import typer
from services.meeting_service import create_meeting, list_meetings, show_meeting

app = typer.Typer()

@app.command("create-meeting")
def create_meeting_cmd(title: str, date: str, owner: str) -> None:
    meeting = create_meeting(title, date, owner)
    typer.echo(f"Created: {meeting.id}")

@app.command("list-meetings")
def list_meetings_cmd() -> None:
    for m in list_meetings():
        typer.echo(f"{m.id} | {m.date} | {m.title}")

@app.command("show-meeting")
def show_meeting_cmd(meeting_id: str) -> None:
    meeting = show_meeting(meeting_id)
    typer.echo(f"Meeting ID: {meeting.id}")
    typer.echo(f"Title: {meeting.title}")
    typer.echo(f"Date: {meeting.date}")
    typer.echo(f"Owner: {meeting.owner}")

if __name__ == "__main__":
    app()