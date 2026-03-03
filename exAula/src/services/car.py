from data.models import Car
from services import storage

def create(registration: str, model: str, price: float, date: str):
    
    newCar = Car(
        registration=registration,
        model=model,
        price=price,
        date=date
    )

    storage.create(car = newCar)