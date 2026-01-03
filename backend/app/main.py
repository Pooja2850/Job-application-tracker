from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List

from .db import Base, engine, SessionLocal
from .models import Application
from .schemas import ApplicationCreate, ApplicationRead

app = FastAPI(title="Job Tracker API")

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/applications", response_model=ApplicationRead)
def create_application(payload: ApplicationCreate, db: Session = Depends(get_db)):
    app_row = Application(**payload.model_dump())
    db.add(app_row)
    db.commit()
    db.refresh(app_row)
    return app_row

@app.get("/applications", response_model=List[ApplicationRead])
def list_applications(db: Session = Depends(get_db)):
    return db.query(Application).order_by(Application.id.desc()).all()
