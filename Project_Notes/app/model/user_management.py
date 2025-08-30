from sqlmodel import SQLModel, Field, Column, Relationship
from typing import Optional, List
from sqlalchemy import String
from datetime import datetime
from pydantic import EmailStr



class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  # Auto-increment
    first_name: str 
    last_name: str 
    email: EmailStr = Field(
        sa_column=Column(String, unique=True, nullable=False, index=True)
    )
    password: str
    # one-to-many relationship with note
    Notes: List["Note"] = Relationship(back_populates="user")

class Note(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")
    
    # Relationship: note → user
    user: Optional[User] = Relationship(back_populates="notes")


class Blacklist(SQLModel, table=True):
    black_token: str = Field(primary_key=True)


