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
    # one-to-many relationship with note
    jobapplications: List["JobApplication"] = Relationship(back_populates="user")

class JobApplication(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    company: str
    position: str
    date_applied: str
    status: str
    user_id: int = Field(foreign_key="user.id")
    
    # Relationship: jobapplications → user
    user: Optional[User] = Relationship(back_populates="jobapplications")


class Blacklist(SQLModel, table=True):
    black_token: str = Field(primary_key=True)


