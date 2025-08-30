#importing the necessary requirement
from pydantic import BaseModel, EmailStr
from datetime import datetime

class Cart(BaseModel):
    product_id: int
    name: str
    price: float
    quantity: float
    

class CartOut(BaseModel):
    id: int
    name: str
    price: float
    quantity: int
    created_at: str
    amount: float

class Order(BaseModel):
    id: int
    name: str
    price: float
    amount: float
    created_at: str
    cart_id: int