from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, JSON, DateTime
from .database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    description = Column(Text)
    location = Column(String)
    skills = Column(String)
    salary = Column(String)


class CV(Base):
    __tablename__ = "cvs"

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String, nullable=False)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    linkedin = Column(String)
    address = Column(String)
    professional_summary = Column(Text)
    skills = Column(Text)
    work_history = Column(JSON)
    education = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)