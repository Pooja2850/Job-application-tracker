from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from .db import Base, engine, SessionLocal
from .models import Application
from .schemas import ApplicationCreate, ApplicationRead

app = FastAPI(title="Job Tracker API")

Base.metadata.create_all(bind=engine)

# Add this schema for updates
class StatusUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None

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

@app.patch("/applications/{app_id}", response_model=ApplicationRead)
def update_application(app_id: int, update: StatusUpdate, db: Session = Depends(get_db)):
    app_row = db.query(Application).filter(Application.id == app_id).first()
    if not app_row:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Update fields if provided
    if update.status is not None:
        app_row.status = update.status
    if update.notes is not None:
        app_row.notes = update.notes
    
    db.commit()
    db.refresh(app_row)
    return app_row