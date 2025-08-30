from pydantic import BaseModel, EmailStr, Field
from typing import Annotated


class Contact(BaseModel):
    name: str
    phone_number:Annotated[str, Field(pattern=r'^\+?[0-9]{7,15}$')]
    email: EmailStr

class ContactOut(BaseModel):
    id: int
    name: str
    phone_number:str
    email: EmailStr
    user_id: int