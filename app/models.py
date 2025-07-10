from sqlalchemy import Column, Integer, String
from .database import Base
from .config import get_config

config = get_config()

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), index=True)
    last_name = Column(String(50), index=True)
    contact_info = Column(String(100), index=True)
    department = Column(String(50), index=True)
    position = Column(String(50), index=True)
    location = Column(String(50), index=True)
    status = Column(String(20), default="active")