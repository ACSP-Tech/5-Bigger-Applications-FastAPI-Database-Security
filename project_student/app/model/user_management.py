from sqlmodel import SQLModel, Field, Relationship, Column
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

class Grade(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    subject: str
    score: float
    student_id: Optional[int] = Field(default=None, foreign_key="student.id")

    student: Optional["Student"] = Relationship(back_populates="grades")

class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: int
    email: EmailStr
    user_id: int = Field(foreign_key="user.id")
    grades: List["Grade"] = Relationship(back_populates="student")

    Grade.student = Relationship(back_populates="grades")

class Blacklist(SQLModel, table=True):
    black_token: str = Field(primary_key=True)