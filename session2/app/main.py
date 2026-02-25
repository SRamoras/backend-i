import typer
from services.memory_store import meetings 

cli = typer.Typer()

@cli.command()
def output():
    typer.echo(meetings)

if __name__ == "__main__":
    cli()   