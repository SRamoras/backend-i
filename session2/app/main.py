import typer
from services.memory_store import meetings 
from domain.models import Meeting, ActionItem
import uuid

cli = typer.Typer()


@cli.command()
def add_metting():
    id = str(uuid.uuid4())

    title = typer.prompt("titulo: ")

    date = typer.prompt("data: ")

    owner = typer.prompt("dono: ")
    
    participantsCounter = typer.prompt("numero de participantes apra adicionar: ")
    participantsList = []
    for i in range(int(participantsCounter)):
        participantName = typer.prompt("nome do participante: ")
        participantsList.append(participantName)

    action_itemsCounter = typer.prompt("numero de reunioes que pretende adicionar: ")
    actionItems = []
    for i in range(int(action_itemsCounter)):
        description = typer.prompt("descricao: ")
        ownerActionItem = typer.prompt("dono: ")
        due_date = typer.prompt("data de entrega ")
        actionItem = ActionItem(description=description, owner=ownerActionItem, due_date=due_date)
        actionItems.append(actionItem)

    metting = Meeting(id=id, title=title, date=date, owner=owner, participants=participantsList, action_items=actionItems)
    meetings.append(metting)


@cli.command()
def show_mettings():
    for meeting in meetings:
        typer.echo("=========== MEETING ===========")
        typer.echo(f"ID: {meeting.id}")
        typer.echo(f"Título: {meeting.title}")
        typer.echo(f"Data: {meeting.date}")
        typer.echo(f"Dono: {meeting.owner}")
        typer.echo(f"Participantes: {meeting.participants}")
        counter = 0
        for action_item in meeting.action_items:
            typer.echo(f"----- ACTION ITEM {counter + 1} -----")
            typer.echo(f"Descrição: {action_item.description}")
            typer.echo(f"Dono: {action_item.owner}")
            typer.echo(f"Data de Entrega: {action_item.due_date}")
            typer.echo(f"Status: {action_item.status}")
            counter += 1
        typer.echo("---------------------------------")

@cli.command()
def add_metting_and_show_mettings():
    add_metting()
    show_mettings()


if __name__ == "__main__":
    cli()