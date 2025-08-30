from sqlmodel import SQLModel, Field, Column, Relationship
from typing import Optional, List, Annotated
from sqlalchemy import String
from datetime import datetime
from pydantic import EmailStr, condecimal, root_validator
from decimal import Decimal



class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  # Auto-increment
    first_name: str 
    last_name: str 
    email: EmailStr = Field(
        sa_column=Column(String, unique=True, nullable=False, index=True)
    )
    role: str
    password: str

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float
    quantity: Annotated[float, condecimal(decimal_places=2)]
    amount: float
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    cart_id: int = Field(foreign_key="cart.id")


class Cart(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float
    quantity: Annotated[float, condecimal(decimal_places=2)]
    Amount: Optional[Decimal] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")

    # auto-compute amount
    @root_validator(pre=True)
    def compute_amount(cls, values):
        price = values.get("price")
        quantity = values.get("quantity")
        if price is not None and quantity is not None:
            values["amount"] = round(Decimal(price) * Decimal(quantity), 2)
        return values

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float
    stock: int

class Blacklist(SQLModel, table=True):
    black_token: str = Field(primary_key=True)

