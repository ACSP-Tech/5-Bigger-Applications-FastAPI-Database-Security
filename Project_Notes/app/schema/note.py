from pydantic import BaseModel
from datetime import datetime


class Note(BaseModel):
    title: str
    content:str

class NoteOut(BaseModel):
    id: int
    title: str
    content:str
    created_at: datetime
    user_id: int