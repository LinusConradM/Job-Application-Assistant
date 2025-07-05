from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import init_db, SessionLocal
from .models import Job
from .schemas import JobSchema
from .tasks import start_scheduler


app = FastAPI(title="Job Application Assistant")


@app.on_event("startup")
def on_startup():
    init_db()
    start_scheduler()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/jobs", response_model=List[JobSchema])
def list_jobs(db: Session = Depends(get_db)):
    return db.query(Job).all()