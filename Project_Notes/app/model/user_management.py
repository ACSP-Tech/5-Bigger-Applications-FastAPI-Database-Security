from sqlmodel import SQLModel, Field, Column, Relationship
from typing import Optional, List
from sqlalchemy import String
from datetime import date
from pydantic import EmailStr



class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  # Auto-increment
    first_name: str 
    last_name: str 
    email: EmailStr = Field(
        sa_column=Column(String, unique=True, nullable=False, index=True)
    )
    password: str


class Note(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    created_at: str
    user_id: int = Field(foreign_key="user.id")


class Blacklist(SQLModel, table=True):
    black_token: str = Field(primary_key=True)


