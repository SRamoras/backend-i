import typer

app = typer.Typer()

@app.command()
def add(title: str, date: str, owner: str) -> None:
    
    typer.echo(f"Hello from Typer!!!")

if __name__ == "__main__":
    app()