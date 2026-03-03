from dataclasses import dataclass

@dataclass
class Car:
    registration: str
    model: str
    price: float 
    date: str
    

    def __str__(self):
        return f"""---
registration: {self.registration}
model: {self.model}
price: {self.price}
date: {self.date}
---
# Car
"""