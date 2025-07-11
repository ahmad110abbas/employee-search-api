from sqlalchemy.orm import Session
from .models import Employee
from .filters import apply_filters
from .cache import generate_cache_key, get_cached_data, set_cached_data
from .schemas import EmployeeSearchRequest
import json

def search_employees_service(
    search_request: EmployeeSearchRequest,
    page: int,
    size: int,
    db: Session
):
    cache_key = generate_cache_key(
        search_request.dict(exclude_none=True),
        page,
        size
    )
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return json.loads(cached_data)

    query = db.query(Employee)
    filters = search_request.dict(exclude_none=True)
    query = apply_filters(query, filters)

    total_count = query.count()
    results = query.offset((page - 1) * size).limit(size).all()

    employees_data = [
        {
            "id": emp.id,
            "first_name": emp.first_name,
            "last_name": emp.last_name,
            "full_name": f"{emp.first_name} {emp.last_name}",
            "contact_info": emp.contact_info,
            "department": emp.department,
            "position": emp.position,
            "location": emp.location,
            "status": emp.status
        }
        for emp in results
    ]

    response = {
        "results": employees_data,
        "pagination": {
            "total": total_count,
            "page": page,
            "size": size,
            "total_pages": (total_count + size - 1) // size
        }
    }

    set_cached_data(cache_key, response)
    return response 