from pydantic import BaseModel, Extra

class EmployeeSearchRequest(BaseModel):
    filters: dict = {}
    class Config:
        extra = Extra.allow  # Allows additional dynamic fields

class EmployeeResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    full_name: str
    contact_info: str
    department: str
    position: str
    location: str
    status: str

class PaginatedResponse(BaseModel):
    results: list[EmployeeResponse]
    pagination: dict