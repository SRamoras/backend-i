from typer import Typer
from services import car_service
from data.models import Car

cli = Typer()


@cli.command()
def create(registration: str, model: str, price: float, date: str):
    newCar = Car(
        registration=registration,
        model=model,
        price=round(price, 2),
        date=date
    )
    car_service.create(car = newCar)


@cli.command()
def list():
    car_service.list()





if __name__ == "__main__":
    cli()
