from services.utils import handle_error
import typer
from services.car_service import create_car, list_cars, delete_car, search_cars, print_cars
from data.models import Car

cli = typer.Typer(help="Car Stand Management CLI application")


@cli.command()
def create_car(registration: str, model: str, price: float, date: str) -> None:
    """
    Creates a new car in the stand.
    """
    newCar = Car(
        registration=registration,
        model=model,
        price=round(price, 2),
        date=date
    )
    create_car(car=newCar)
    print(f"Car '{registration}' created successfully")



@cli.command()
def list_cars() -> None:
    """
    Lists all cars registered in the stand.
    """
    def action():
        cars = list_cars()
        print_cars(cars)

    handle_error(action)



@cli.command()
def delete_car(registration: str) -> None:
    """
    Deletes a car from the stand.
    """
    def action():
        delete_car(registration)
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

    Filters:
    - registration: search by registration number
    - model: search by car model
    - min_price: minimum price filter
    - max_price: maximum price filter
    """

    def action() -> None:
        cars = search_cars(registration, model, min_price, max_price)
        print_cars(cars)

    handle_error(action)



if __name__ == "__main__":
    cli()
