from os import name
from typing import Optional
from pydantic import BaseModel

class Customer(BaseModel):
    id: int
    name: str
    email: Optional[str] = None 
    customer_since: str
    phone: Optional[str] = None
    customer_id: str
    points: int = 0
    orders: int = 0
