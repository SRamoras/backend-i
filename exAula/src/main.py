import typer
from services import car_service
from data.models import Car

cli = typer.Typer()


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
def listCars():
    car_service.listCars()


@cli.command()
def delete(registration: str):
    car_service.delete(registration)


@cli.command()
def search(
    registration: str = None,
    model: str = None,
    min_price: float = None,
    max_price: float = None
):
    car_service.searchCars(registration, model, min_price, max_price)

if __name__ == "__main__":
    cli()
