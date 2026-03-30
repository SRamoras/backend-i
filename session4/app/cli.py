import typer
from services import meeting, database

cli = typer.Typer()


@cli.command()
def create(
    title: str = typer.Option(..., "--title"),
    owner: str = typer.Option(..., "--owner"),
    date: str  = typer.Option(..., "--date"),
) -> None:
    meeting.create(title, owner, date)
    typer.secho("✅ Reunião criada!", fg=typer.colors.GREEN, bold=True)


@cli.command()
def list_meetings() -> None:
    meetings = database.list_meetings()
    if not meetings:
        typer.echo("Nenhuma reunião encontrada.")
        raise typer.Exit()
    for m in meetings:
        typer.echo(f"{m.date} | {m.title} | {m.owner} | {len(m.action_items)} action items")


@cli.command()
def export_csv() -> None:
    database.export_csv()
    typer.secho("✅ CSV exportado para meetings/report.csv", fg=typer.colors.GREEN)


if __name__ == "__main__":
    cli()