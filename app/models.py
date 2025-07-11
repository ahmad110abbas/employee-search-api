from sqlalchemy import Column, Integer, String, Enum as SqlEnum
from enum import Enum
from .database import Base
from .config import get_config

config = get_config()

class EmployeeStatus(str, Enum):
    active = "active"
    not_started = "not_started"
    terminated = "terminated"

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), index=True)
    last_name = Column(String(50), index=True)
    contact_info = Column(String(100), index=True)
    department = Column(String(50), index=True)
    position = Column(String(50), index=True)
    location = Column(String(50), index=True)
    organization = Column(String(100), index=True, nullable=True)
    status = Column(SqlEnum(EmployeeStatus), default=EmployeeStatus.active, nullable=False)