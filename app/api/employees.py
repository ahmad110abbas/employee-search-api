from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.employee import EmployeeSearchRequest, PaginatedResponse
from app.services.employee_service import search_employees_service

router = APIRouter()

@router.post(
    "/employees/search", 
    response_model=PaginatedResponse,
    summary="Search Employees",
    description="""
    Search and filter employees based on various criteria.
    
    **Features:**
    - Filter by name (first_name, last_name, full_name)
    - Filter by department, position, location, organization
    - Filter by status (active, not_started, terminated)
    - Pagination support with customizable page size
    - Intelligent caching for improved performance
    
    **Example Usage:**
    ```json
    {
        "first_name": "John",
        "department": "Engineering",
        "status": "active"
    }
    ```
    """,
    response_description="Paginated list of employees matching the search criteria",
    tags=["employees"]
)
async def search_employees(
    search_request: EmployeeSearchRequest = Body(
        ...,
        description="Search criteria for filtering employees",
        example={
            "first_name": "John",
            "department": "Engineering", 
            "status": "active",
            "organization": "Tech Corp"
        }
    ),
    page: int = Query(
        1, 
        ge=1, 
        description="Page number (starts from 1)",
        example=1
    ),
    size: int = Query(
        10, 
        ge=1, 
        le=100, 
        description="Number of employees per page (max 100)",
        example=10
    ),
    db: Session = Depends(get_db)
):
    """
    Search employees with advanced filtering and pagination.
    
    This endpoint allows you to search for employees using various filters:
    - **Text filters**: first_name, last_name, full_name, contact_info
    - **Categorical filters**: department, position, location, organization  
    - **Status filter**: active, not_started, terminated
    
    All filters are optional and can be combined for precise searches.
    """
    return search_employees_service(
        search_request=search_request,
        page=page,
        size=size,
        db=db
    ) 