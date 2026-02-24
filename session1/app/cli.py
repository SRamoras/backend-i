import typer
import datetime

app = typer.Typer()

@app.command()
def create_meeting(title: str, date: str, owner: str) -> None:
    try:
        datetime.date.fromisoformat(date)
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")

    print(title, date, owner)
    typer.echo(f"Hello from Typer!!!")

if __name__ == "__main__":
    app()