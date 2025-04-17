from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.database import SessionLocal, engine
from app.models import Base
from routers import upload
from routers import image_upload
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request

templates = Jinja2Templates(directory="app/templates")
# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/staff/", response_model=List[schemas.StaffResponse])
def get_all_staff(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    return crud.get_all_staff(db=db, skip=skip, limit=limit)

@app.get("/staff/{staff_id}", response_model=schemas.StaffResponse)
def get_staff_by_id(staff_id: int, db: Session = Depends(get_db)):
    db_staff = crud.get_staff_by_id(db, staff_id)
    if db_staff is None:
        raise HTTPException(status_code=404, detail="Staff not found")
    return db_staff

@app.post("/staff/", response_model=schemas.StaffResponse)
def create_staff(staff: schemas.StaffCreate, db: Session = Depends(get_db)):
    return crud.create_staff(db=db, staff=staff)


app.include_router(upload.router)
app.include_router(image_upload.router)
app.mount("/uploaded_images", StaticFiles(directory="uploaded_images"), name="uploaded_images")

@app.get("/dashboard", response_class=HTMLResponse)
def image_dashboard(request: Request):
    return templates.TemplateResponse("image_dashboard.html", {"request": request})
