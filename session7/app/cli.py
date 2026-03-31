import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import typer
from core.logging_config import configure_logging
from core.exception_handler import handle_exception
from services import action_item_service as svc
from services.report_service import summary, period_report

configure_logging()
app = typer.Typer()

@app.command()
def create(
    title: str,
    owner: str = typer.Option(...),
    due_date: str = typer.Option(...),
):
    try:
        item = svc.create_action_item(title, owner, due_date)
        typer.echo(f"Created: {item}")
    except Exception as exc:
        code, message = handle_exception(exc)
        typer.echo(f"Error: {message}")
        raise typer.Exit(code=code)

@app.command()
def list():
    items = svc.list_action_items()
    if not items:
        typer.echo("No items found.")
        return
    for item in items:
        typer.echo(f"[{item.id}] {item.title} — {item.owner} — {item.due_date}")

@app.command()
def show(id: str = typer.Option(...)):
    try:
        item = svc.get_action_item(id)
        typer.echo(item)
    except Exception as exc:
        code, message = handle_exception(exc)
        typer.echo(f"Error: {message}")
        raise typer.Exit(code=code)

@app.command()
def delete(id: str = typer.Option(...)):
    try:
        svc.delete_action_item(id)
        typer.echo(f"Deleted: {id}")
    except Exception as exc:
        code, message = handle_exception(exc)
        typer.echo(f"Error: {message}")
        raise typer.Exit(code=code)

@app.command()
def report():
    items = svc.list_action_items()
    typer.echo(summary(items))

@app.command()
def report_period(
    from_date: str = typer.Option(...),
    to_date: str = typer.Option(...),
):
    items = svc.list_action_items()
    typer.echo(period_report(items, from_date, to_date))

if __name__ == "__main__":
    app()