#importing the necessary requirement
from pydantic import BaseModel, EmailStr

class Product(BaseModel):
    name: str
    price: float
    stock: int

class ProductOut(BaseModel):
    id: int
    name: str
    price: float
    stock: int