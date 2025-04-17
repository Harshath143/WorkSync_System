from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Staff(Base):
    __tablename__ = "staffs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    role = Column(String, default="Employee")

    sessions = relationship("WorkSession", back_populates="staff")


class WorkSession(Base):
    __tablename__ = "work_sessions"

    id = Column(Integer, primary_key=True, index=True)
    staff_id = Column(Integer, ForeignKey("staffs.id"))
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    is_working = Column(Boolean, default=True)

    staff = relationship("Staff", back_populates="sessions")

# app/models.py
class CapturedImage(Base):
    __tablename__ = "captured_images"

    id = Column(Integer, primary_key=True, index=True)
    image_path = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    staff_id = Column(Integer, ForeignKey("staffs.id"))
    session_id = Column(Integer, ForeignKey("work_sessions.id"))

    staff = relationship("Staff")
    session = relationship("WorkSession")
