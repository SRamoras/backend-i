import typer
from services.action_item_service import create_action_item
from core.exception_handler import handle_exception

app = typer.Typer()


@app.command()
def create(
    title: str,
    owner: str = typer.Option(None),
    due_date: str = typer.Option(None),
):
    try:
        item = create_action_item(title, owner, due_date)
        typer.echo(f"Created: {item}")

    except Exception as exc:
        code, message = handle_exception(exc)
        typer.echo(f"Error: {message}")
        raise typer.Exit(code=code)


if __name__ == "__main__":
    app()