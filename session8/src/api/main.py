from fastapi import FastAPI

api = FastAPI()

@api.get("/shop")
def list_products():
    ...