#importing the necessary requirement
from pydantic import BaseModel, EmailStr
from typing import List


# input schema for grade (no id because client doesn’t send it)
class GradeCreate(BaseModel):
    subject: str
    score: float

# input schema for student
class StudentCreate(BaseModel):
    name: str
    age: int
    email: EmailStr
    grades: List[GradeCreate]

# output schema for grade
class GradeRead(BaseModel):
    id: int
    subject: str
    score: float

# output schema for student (with nested grades)
class StudentRead(BaseModel):
    id: int
    name: str
    age: int
    email: EmailStr
    grades: List[GradeRead]

# input schema for student update
class StudentUpdate(BaseModel):
    name: str
    age: int