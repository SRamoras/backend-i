from typer import Typer
from api.main import api
import uvicorn


cli = Typer()

@cli.command()
def run():
    uvicorn.run(api, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    cli()
    