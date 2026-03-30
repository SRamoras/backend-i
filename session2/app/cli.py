import typer
from services.memory_store import meetings
from domain.models import Meeting, ActionItem
import uuid

cli = typer.Typer()


@cli.command()
def add_meeting():
    meeting_id = str(uuid.uuid4())

    title = typer.prompt("titulo: ")
    date = typer.prompt("data: ")
    owner = typer.prompt("dono: ")

    participants_counter = typer.prompt("numero de participantes para adicionar: ")
    participants_list = []
    for i in range(int(participants_counter)):
        participant_name = typer.prompt("nome do participante: ")
        participants_list.append(participant_name)

    action_items_counter = typer.prompt("numero de action items para adicionar: ")
    action_items = []
    for i in range(int(action_items_counter)):
        description = typer.prompt("descricao: ")
        owner_action_item = typer.prompt("dono: ")
        due_date = typer.prompt("data de entrega: ")
        action_item = ActionItem(description=description, owner=owner_action_item, due_date=due_date)
        action_items.append(action_item)

    meeting = Meeting(id=meeting_id, title=title, date=date, owner=owner, participants=participants_list, action_items=action_items)
    meetings.append(meeting)


@cli.command()
def show_meetings():
    for meeting in meetings:
        typer.echo("=========== MEETING ===========")
        typer.echo(f"ID: {meeting.id}")
        typer.echo(f"Título: {meeting.title}")
        typer.echo(f"Data: {meeting.date}")
        typer.echo(f"Dono: {meeting.owner}")
        typer.echo(f"Participantes: {meeting.participants}")
        for counter, action_item in enumerate(meeting.action_items, start=1):
            typer.echo(f"----- ACTION ITEM {counter} -----")
            typer.echo(f"Descrição: {action_item.description}")
            typer.echo(f"Dono: {action_item.owner}")
            typer.echo(f"Data de Entrega: {action_item.due_date}")
            typer.echo(f"Status: {action_item.status}")
        typer.echo("---------------------------------")


if __name__ == "__main__":
    cli()