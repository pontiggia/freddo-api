from fastapi import FastAPI
from src.routes.customer import customer

app = FastAPI()

app.include_router(customer, prefix="/customer")

