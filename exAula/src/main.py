from typer import Typer
from services import car_service
from data.models import Car

cli = Typer()


@cli.command()
def create(registration: str, model: str, price: float, date: str):
    newCar = Car(
        registration=registration,
        model=model,
        price=price,
        date=date
    )
    car_service.create(car = newCar)

if __name__ == "__main__":
    cli()
