from sqlmodel import SQLModel, Field, Column, Relationship
from pydantic import EmailStr
from typing import Optional, List
from sqlalchemy import String



class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  # Auto-increment
    first_name: str 
    last_name: str 
    email: EmailStr = Field(
        sa_column=Column(String, unique=True, nullable=False, index=True)
    )
    password: str
    # one-to-many relationship with Contact
    contacts: List["Contact"] = Relationship(back_populates="user")

class Contact(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    phone_number: str
    email: EmailStr
    user_id: int = Field(foreign_key="user.id")
    
    # Relationship: contact → user
    user: Optional[User] = Relationship(back_populates="contacts")


class Blacklist(SQLModel, table=True):
    black_token: str = Field(primary_key=True)


#User.contacts