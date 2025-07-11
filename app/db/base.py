from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///../employees.db", connect_args={"check_same_thread": False})
Base = declarative_base() 