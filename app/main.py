
import uuid
import shutil
from pathlib import Path

import logging
from typing import List


from typing import List
from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from .config import settings
from .database import init_db, SessionLocal
from .models import CV, Job
from .schemas import CVSchema, JobSchema
from .tasks import start_scheduler
from .utils import parse_cv_file


app = FastAPI(title="Job Application Assistant")
logging.basicConfig(level=logging.INFO)


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


@app.post("/cvs", response_model=CVSchema)
def upload_cv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type not in (
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain",
    ):
        raise HTTPException(400, "Invalid file type")
    upload_path = Path(settings.UPLOAD_DIR)
    upload_path.mkdir(parents=True, exist_ok=True)
    ext = Path(file.filename).suffix.lower()
    filename = f"{uuid.uuid4()}{ext}"
    file_path = upload_path / filename
    with open(file_path, "wb") as out_file:
        shutil.copyfileobj(file.file, out_file)
    data = parse_cv_file(str(file_path))
    cv = CV(file_path=str(file_path), **data)
    db.add(cv)
    db.commit()
    db.refresh(cv)
    return cv