from sqlalchemy import or_, func
from .models import Employee

def apply_filters(query, filters: dict):
    for field, value in filters.items():
        if not hasattr(Employee, field):
            continue
            
        column = getattr(Employee, field)
        
        if isinstance(value, list):
            if field == "status":
                valid_statuses = [s for s in value if s in ["active","not_started","terminated"]]
                if valid_statuses:
                    query = query.filter(column.in_(valid_statuses))
            else:
                query = query.filter(column.in_(value))
        else:
            if field == "status":
                if value in ["active","not_started","terminated"]:
                    query = query.filter(column == value)
            else:
                query = query.filter(column == value)
    
    if "full_name" in filters:
        search_value = filters["full_name"]
        
        if isinstance(search_value, list):
            or_conditions = []
            for name in search_value:
                name = f"%{name}%"
                or_conditions.append(Employee.first_name.ilike(name))
                or_conditions.append(Employee.last_name.ilike(name))
                or_conditions.append(func.concat(Employee.first_name, ' ', Employee.last_name).ilike(name))
            query = query.filter(or_(*or_conditions))
        else:
            name = f"%{search_value}%"
            query = query.filter(
                or_(
                    Employee.first_name.ilike(name),
                    Employee.last_name.ilike(name),
                    func.concat(Employee.first_name, ' ', Employee.last_name).ilike(name)
                )
            )
    
    return query