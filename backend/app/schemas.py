from pydantic import BaseModel
from datetime import date
from typing import Optional

class ApplicationCreate(BaseModel):
    company: str
    role_title: str
    location: Optional[str] = None
    link: Optional[str] = None
    date_applied: Optional[date] = None
    status: str = "Applied"
    tags: Optional[str] = None
    notes: Optional[str] = None

class ApplicationRead(ApplicationCreate):
    id: int

    class Config:
        from_attributes = True