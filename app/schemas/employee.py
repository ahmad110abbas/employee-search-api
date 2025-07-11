from typing import Optional
from pydantic import BaseModel, Extra
from app.db.models import EmployeeStatus

class EmployeeSearchRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
    contact_info: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    location: Optional[str] = None
    organization: Optional[str] = None
    status: Optional[EmployeeStatus] = None

    class Config:
        extra = Extra.forbid  # Forbid additional fields

class EmployeeResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    full_name: str
    contact_info: str
    department: str
    position: str
    location: str
    organization: str
    status: EmployeeStatus

class PaginatedResponse(BaseModel):
    results: list[EmployeeResponse]
    pagination: dict 