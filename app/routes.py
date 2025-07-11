from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from .database import get_db
from .schemas import EmployeeSearchRequest, PaginatedResponse
from .services import search_employees_service

router = APIRouter()

@router.post("/employees/search", response_model=PaginatedResponse)
async def search_employees(
    search_request: EmployeeSearchRequest,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return search_employees_service(
        search_request=search_request,
        page=page,
        size=size,
        db=db
    )