from sqlalchemy.orm import Session
from app import models, schemas

def get_all_staff(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Staff).offset(skip).limit(limit).all()

def get_staff_by_id(db: Session, staff_id: int):
    return db.query(models.Staff).filter(models.Staff.id == staff_id).first()

def create_staff(db: Session, staff: schemas.StaffCreate):
    db_staff = models.Staff(name=staff.name, email=staff.email, role=staff.role)
    db.add(db_staff)
    db.commit()
    db.refresh(db_staff)
    return db_staff
