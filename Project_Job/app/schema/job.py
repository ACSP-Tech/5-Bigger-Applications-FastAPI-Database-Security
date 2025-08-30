from pydantic import BaseModel
from datetime import date


class JobApplication(BaseModel):
    company: str
    position: str
    date_applied: date
    status: str

class JobApplicationOut(BaseModel):
    id: int
    company: str
    position: str
    date_applied: date
    status: str
    user_id: int