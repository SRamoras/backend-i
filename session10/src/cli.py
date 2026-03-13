import typer
import uvicorn

from api.main import api

app = typer.Typer()

@app.command()
def run():
    uvicorn.run(api, host="0.0.0.0")

@app.command()
def test():
    ...

if __name__ == "__main__":
    app()