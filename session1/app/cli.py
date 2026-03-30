import typer
import datetime

app = typer.Typer()

@app.command("create-meeting")
def create_meeting(
    title: str = typer.Option(..., "--title", help="Título da reunião"),
    date: str  = typer.Option(..., "--date",  help="Data no formato YYYY-MM-DD"),
    owner: str = typer.Option(..., "--owner", help="Responsável pela reunião"),
) -> None:
    try:
        datetime.date.fromisoformat(date)
    except ValueError:
        typer.echo("❌ O formato da data está errado. Tem de ser YYYY-MM-DD", err=True)
        raise typer.Exit(code=1)

    typer.secho(f"✅ Reunião criada!", fg=typer.colors.GREEN, bold=True)
    typer.echo(f"   Título : {title}")
    typer.echo(f"   Data   : {date}")
    typer.echo(f"   Owner  : {owner}")

if __name__ == "__main__":
    app()