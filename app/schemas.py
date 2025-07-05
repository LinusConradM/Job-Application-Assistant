from pydantic import BaseModel
from typing import Optional


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