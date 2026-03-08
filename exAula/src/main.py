from services.utils import handle_error
import typer
from services import car_service
from data.models import Car
from datetime import datetime
cli = typer.Typer(help="Car Stand Management CLI application")

from datetime import datetime
from datetime import datetime

@cli.command()
def create_car(
    registration: str,
    model: str,
    price: float,
    date: str,
) -> None:
    """
    Creates a new car in the stand.
    """

    def action():

        parsed_date = datetime.strptime(date, "%d-%m-%Y")

        newCar = Car(
            registration=registration,
            model=model,
            price=round(price, 2),
            date=parsed_date.strftime("%d-%m-%Y"),
        )

        car_service.create_car(newCar)

        print(f"Car '{registration}' created successfully")

    handle_error(action)

@cli.command()
def list_cars() -> None:
    """
    Lists all cars registered in the stand.
    """
    def action():
        cars = car_service.list_cars()
        car_service.print_cars(cars)

    handle_error(action)


@cli.command()
def delete_car(registration: str) -> None:
    """
    Deletes a car from the stand.
    """
    def action():
        car_service.delete_car(registration)
        print(f"Car '{registration}' removed successfully")

    handle_error(action)


@cli.command()
def search_cars(
    registration: str | None = None,
    model: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None
) -> None:
    """
    Searches for cars in the stand using optional filters.
    """

    def action():
        cars = car_service.search_cars(registration, model, min_price, max_price)
        car_service.print_cars(cars)

    handle_error(action)


@cli.command()
def update_car(
    registration: str,
    model: str | None = None,
    price: float | None = None,
    date: str | None = None
) -> None:
    """
    Updates an existing car.
    """

    def action():
        car_service.update_car(registration, model, price, date)
        print(f"Car '{registration}' updated successfully")

    handle_error(action)


if __name__ == "__main__":
    cli()