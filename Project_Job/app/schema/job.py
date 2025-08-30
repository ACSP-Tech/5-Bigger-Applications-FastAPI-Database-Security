from pydantic import BaseModel
from datetime import datetime


class JobApplication(BaseModel):
    title: str
    content:str

class JobApplicationOut(BaseModel):
    id: int
    title: str
    content:str
    created_at: datetime
    user_id: int