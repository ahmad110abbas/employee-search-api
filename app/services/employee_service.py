import logging
from sqlalchemy.orm import Session
from app.db.models import Employee
from app.filters import apply_filters
from app.cache import generate_cache_key, get_cached_data, set_cached_data
from app.schemas.employee import EmployeeSearchRequest
import json

logger = logging.getLogger(__name__)

def search_employees_service(
    search_request: EmployeeSearchRequest,
    page: int,
    size: int,
    db: Session
):
    logger.info(f"Employee search request: filters={search_request.dict(exclude_none=True)}, page={page}, size={size}")
    cache_key = generate_cache_key(
        search_request.dict(exclude_none=True),
        page,
        size
    )
    cached_data = get_cached_data(cache_key)
    if cached_data:
        logger.info(f"Cache hit for key: {cache_key}")
        return json.loads(cached_data)
    logger.info(f"Cache miss for key: {cache_key}")
    try:
        query = db.query(Employee)
        filters = search_request.dict(exclude_none=True)
        query = apply_filters(query, filters)
        total_count = query.count()
        results = query.offset((page - 1) * size).limit(size).all()
    except Exception as e:
        logger.error(f"Database error during employee search: {e}", exc_info=True)
        raise

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
            "organization": emp.organization,
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