import typer
from services.meeting_service import create_meeting, list_meetings, get_meeting

cli = typer.Typer()


@cli.command()
def add_meeting(
    title: str = typer.Option(..., "--title", help="Título da reunião"),
    date: str  = typer.Option(..., "--date",  help="Data no formato YYYY-MM-DD"),
    owner: str = typer.Option(..., "--owner", help="Responsável pela reunião"),
) -> None:
    meeting = create_meeting(title=title, date=date, owner=owner)
    typer.secho("✅ Reunião criada!", fg=typer.colors.GREEN, bold=True)
    typer.echo(f"   ID    : {meeting.id}")
    typer.echo(f"   Título: {meeting.title}")
    typer.echo(f"   Data  : {meeting.date}")
    typer.echo(f"   Owner : {meeting.owner}")


@cli.command()
def show_meetings() -> None:
    meetings = list_meetings()
    if not meetings:
        typer.echo("Nenhuma reunião encontrada.")
        raise typer.Exit()
    for m in meetings:
        typer.echo(f"{m.id} | {m.date} | {m.title}")


@cli.command()
def show_meeting(
    meeting_id: str = typer.Option(..., "--id", help="ID da reunião"),
) -> None:
    meeting = get_meeting(meeting_id)
    if not meeting:
        typer.secho("❌ Reunião não encontrada.", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)
    typer.echo(f"ID    : {meeting.id}")
    typer.echo(f"Título: {meeting.title}")
    typer.echo(f"Data  : {meeting.date}")
    typer.echo(f"Owner : {meeting.owner}")


if __name__ == "__main__":
    cli()