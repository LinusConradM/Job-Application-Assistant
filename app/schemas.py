from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class JobSchema(BaseModel):
    id: int
    title: str
    company: str
    description: Optional[str]
    location: Optional[str]
    skills: Optional[str]
    salary: Optional[str]

    class Config:
        orm_mode = True


class CVSchema(BaseModel):
    id: int
    file_path: str
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    linkedin: Optional[str]
    address: Optional[str]
    professional_summary: Optional[str]
    skills: Optional[str]
    work_history: Optional[List[dict]]
    education: Optional[List[dict]]
    created_at: datetime

    class Config:
        orm_mode = True