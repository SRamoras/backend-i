from data.models import Car
from uuid import uuid4
from pathlib import Path
from dataclasses import asdict
import json


BASE_PATH = Path("stand")
INDEX_PATH = Path(BASE_PATH/"index_stand.json")


def create(car: Car):
    
    carFile = f"{BASE_PATH}/{uuid4()}.md"

    with open(carFile, "w") as file:
        file.writelines(str(car))

    if not INDEX_PATH.exists():
        INDEX_PATH.touch()
        INDEX_PATH.write_text("[]")

    with open(INDEX_PATH, "r") as file:
        indexFileContent:list = json.load(file)

    newIdex = asdict(
        Car(
            registration=car.registration,
            model=car.model,
            price=car.price,
            date=car.date,
        )
    )
    indexFileContent.append(newIdex)


    with open(INDEX_PATH, "w") as file:
        json.dump(indexFileContent, file)


def list():
    with open(INDEX_PATH, "r") as file:
        indexFileContent:list = json.load(file)

    count = 0
    for car in indexFileContent:
        count += 1
        print(f"{count}) matricula: {car['registration']} - preço: {car['price']}€")