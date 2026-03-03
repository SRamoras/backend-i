from typer import Typer
from services import car
from data.models import Car
cli = Typer()


@cli.command()
def create(registration: str, model: str, price: float, date: str):
    car.create(registration, model, price, date)

if __name__ == "__main__":
    cli()
