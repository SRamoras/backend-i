from data.models import Car
from uuid import uuid4
from pathlib import Path
from dataclasses import asdict
from .utils import ensureJson, saveJson

BASE_PATH = Path("stand")
INDEX_PATH = Path(BASE_PATH/"index_stand.json")


def create(car: Car):
    carFile = f"{BASE_PATH}/{uuid4()}.md"
   
    with open(carFile, "w") as file:
        file.writelines(str(car))

    indexFileContent = ensureJson(INDEX_PATH)

    newIdex = asdict(
        Car(
            registration=car.registration,
            model=car.model,
            price=car.price,
            date=car.date,
        )
    )
    indexFileContent.append(newIdex)
    saveJson(INDEX_PATH, indexFileContent)



def listCars():
    index_file_content = ensureJson(INDEX_PATH)
    if not index_file_content:
        print("Nenhum carro cadastrado")
        return

    for idx, car in enumerate(index_file_content, start=1):
        print(f"{idx}) Matrícula: {car['registration']} - Modelo: {car['model']} - Preço: {car['price']}€")


def delete(registration: str):
    index_file_content = ensureJson(INDEX_PATH)
    
    existe = any(c["registration"] == registration for c in index_file_content)
    if not existe:
        print(f"Nenhum carro com a matrícula '{registration}' encontrado ❌")
        return

    index_file_content = [c for c in index_file_content if c["registration"] != registration]
    saveJson(INDEX_PATH, index_file_content)
    print(f"Carro com matrícula '{registration}' removido com sucesso ✅")


def searchCars(registration: str = None, model: str = None, min_price: float = None, max_price: float = None):
    """
    Search cars by registration, model, or price range.
    """
    index_file_content = ensureJson(INDEX_PATH)

    if not index_file_content:
        print("Nenhum carro cadastrado 😕")
        return

    results = index_file_content

    if registration:
        results = [c for c in results if registration.lower() in c["registration"].lower()]
    if model:
        results = [c for c in results if model.lower() in c["model"].lower()]
    if min_price is not None:
        results = [c for c in results if c["price"] >= min_price]
    if max_price is not None:
        results = [c for c in results if c["price"] <= max_price]

    if not results:
        print("Nenhum carro encontrado com os filtros fornecidos 😕")
        return

    for idx, car in enumerate(results, start=1):
        print(f"{idx}) Matrícula: {car['registration']} - Modelo: {car['model']} - Preço: {car['price']}€")