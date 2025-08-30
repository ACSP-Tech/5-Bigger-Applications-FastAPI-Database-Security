#pydantic validation of user details in respect to frontend Body Field and reponse sent out

#importing the necessary requirement
from pydantic import BaseModel, EmailStr

class Login(BaseModel):
    email: EmailStr
    password:str

class Register(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password:str

class RegisterOut(BaseModel): 
    id: int
    last_name: str
    first_name: str
    email: str