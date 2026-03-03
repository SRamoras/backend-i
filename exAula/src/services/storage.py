from data.models import Car
from uuid import uuid4
from pathlib import Path
from dataclasses import asdict
import json


BASE_PATH = Path("stand")
INDEX_PATH = BASE_PATH/"index_stand.json"


def create(car: Car):
    
    carFile = f"{BASE_PATH}/{uuid4()}.md"


    with open(carFile, "w") as file:
        file.writelines(str(car))
