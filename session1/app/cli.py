import typer
import datetime

app = typer.Typer()

@app.command()
def create_meeting(title: str, date: str, owner: str) -> None:
    try:
        datetime.date.fromisoformat(date)
    except ValueError:
        print("O formato da data está errado. Tem de ser YYYY-MM-DD")
        raise typer.Exit(code=1)

    print(title, date, owner)
    typer.echo(f"Hello from Typer!!!")

if __name__ == "__main__":
    app()