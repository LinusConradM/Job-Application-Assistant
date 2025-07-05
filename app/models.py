from sqlalchemy import Column, Integer, String, Text

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