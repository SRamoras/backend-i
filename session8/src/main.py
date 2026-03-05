from typer import Typer
from api.main import api
import uvicorn

app = Typer()


@app.command()
def run():
    uvicorn.run(api)




if __name__ == "__main__":
    app()