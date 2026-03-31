import typer
import uvicorn

app = typer.Typer()


@app.command()
def run():
    uvicorn.run("api.main:api", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    app()
