from sqlmodel import SQLModel, Field, Column, Relationship
from typing import Optional, List, Annotated
from sqlalchemy import String
from datetime import datetime
from pydantic import EmailStr, condecimal, root_validator
from decimal import Decimal

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float
    stock: int

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  # Auto-increment
    first_name: str 
    last_name: str 
    email: EmailStr = Field(
        sa_column=Column(String, unique=True, nullable=False, index=True)
    )
    role: str
    password: str

class Cart(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float
    quantity: Annotated[float, condecimal(decimal_places=2)]
    amount: Annotated[float, condecimal(decimal_places=2)]
    created_at: str
    user_id: int = Field(foreign_key="user.id")
    product_id: int = Field(foreign_key="product.id")

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float
    quantity: Annotated[float, condecimal(decimal_places=2)]
    amount: float
    created_at: str
    cart_id: int = Field(foreign_key="cart.id")
    user_id: int = Field(foreign_key="user.id")


class Blacklist(SQLModel, table=True):
    black_token: str = Field(primary_key=True)

