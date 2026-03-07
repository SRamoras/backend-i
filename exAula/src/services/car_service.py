from data.models import Car
from uuid import uuid4
from pathlib import Path
from dataclasses import asdict
from .utils import ensureJson, saveJson

BASE_PATH = Path("stand")
INDEX_PATH = Path(BASE_PATH / "index_stand.json")


def create_car(car: Car) -> None:
    """
    Creates a new car entry.

    This function:
    - Generates a unique markdown file for the car.
    - Saves the car information in the stand directory.
    - Updates the JSON index file with the new car.

    Args:
        car (Car): Car object containing registration, model, price and date.
    """

    carFile = f"{BASE_PATH}/{uuid4()}.md"

    with open(carFile, "w") as file:
        file.writelines(str(car))

    indexFileContent = ensureJson(INDEX_PATH)

    newIndex = asdict(car)

    indexFileContent.append(newIndex)
    saveJson(INDEX_PATH, indexFileContent)


def list_cars() -> list[dict]:
    """
    Retrieves all cars stored in the stand.

    Returns:
        list[dict]: A list of dictionaries representing the cars stored in the JSON index.

    Raises:
        ValueError: If no cars are registered in the stand.
    """

    cars = ensureJson(INDEX_PATH)

    if not cars:
        raise ValueError("No cars registered in the stand")

    return cars


def delete_car(registration: str) -> None:
    """
    Deletes a car from the stand using its registration number.

    Args:
        registration (str): The registration number of the car to delete.

    Raises:
        ValueError: If no car with the given registration exists.
    """

    index_file_content = ensureJson(INDEX_PATH)

    exists = any(c["registration"] == registration for c in index_file_content)

    if not exists:
        raise ValueError(f"Car with registration '{registration}' not found")

    index_file_content = [
        c for c in index_file_content if c["registration"] != registration
    ]

    saveJson(INDEX_PATH, index_file_content)


def search_cars(
    registration: str = None,
    model: str = None,
    min_price: float = None,
    max_price: float = None,
) -> list[dict]:
    """
    Searches for cars using optional filters.

    Filters can be applied by:
    - registration (partial match)
    - model (partial match)
    - minimum price
    - maximum price

    Args:
        registration (str | None): Registration filter.
        model (str | None): Model filter.
        min_price (float | None): Minimum price filter.
        max_price (float | None): Maximum price filter.

    Returns:
        list[dict]: List of cars matching the filters.

    Raises:
        ValueError: If no cars exist or no cars match the filters.
    """

    index_file_content = ensureJson(INDEX_PATH)

    if not index_file_content:
        raise ValueError("No cars registered in the stand")

    results = index_file_content

    if registration:
        results = [
            c for c in results
            if registration.lower() in c["registration"].lower()
        ]

    if model:
        results = [
            c for c in results
            if model.lower() in c["model"].lower()
        ]

    if min_price is not None:
        results = [
            c for c in results
            if c["price"] >= min_price
        ]

    if max_price is not None:
        results = [
            c for c in results
            if c["price"] <= max_price
        ]

    if not results:
        raise ValueError("No cars found with the provided filters")

    return results


def update_car(
    registration: str,
    model: str | None = None,
    price: float | None = None,
    date: str | None = None
) -> None:
    """
    Updates an existing car using its registration.

    Only the provided fields will be updated.

    Args:
        registration (str): Registration of the car to update
        model (str | None): New model
        price (float | None): New price
        date (str | None): New date

    Raises:
        ValueError: If the car does not exist
    """

    cars = ensureJson(INDEX_PATH)

    car = next((c for c in cars if c["registration"] == registration), None)

    if not car:
        raise ValueError(f"Car with registration '{registration}' not found")

    if model is not None:
        car["model"] = model

    if price is not None:
        car["price"] = round(price, 2)

    if date is not None:
        car["date"] = date

    saveJson(INDEX_PATH, cars)


def print_cars(cars: list[dict]) -> None:
    """
    Prints a formatted list of cars.

    Args:
        cars (list[dict]): List of cars to display.
    """

    for idx, car in enumerate(cars, start=1):
        print(
            f"{idx}) Matrícula: {car['registration']} - "
            f"Modelo: {car['model']} - "
            f"Preço: {car['price']}€"
        )