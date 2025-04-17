from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class WorkSessionBase(BaseModel):
    start_time: datetime
    end_time: Optional[datetime] = None
    is_working: bool

class WorkSessionCreate(WorkSessionBase):
    staff_id: int

class WorkSessionResponse(WorkSessionBase):
    id: int
    staff_id: int

    class Config:
        orm_mode = True

class StaffBase(BaseModel):
    name: str
    email: str
    role: Optional[str] = "Employee"

class StaffCreate(StaffBase):
    pass

class StaffResponse(StaffBase):
    id: int
    sessions: List[WorkSessionResponse] = []

    class Config:
        orm_mode = True
