from sqlalchemy import Column, Integer, String, Date, BigInteger, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from datetime import date


# Define Pydantic models
class EmployeeDetails(BaseModel):
    id: str
    name: str
    salary: float
    dept: str
    contact_number: int
    gender: str
    dob: date
    position: str
    user_name: str
    user_pass: str


class UserCredentials(BaseModel):
    user_name: str
    user_pass: str


# Define SQLAlchemy model
Base = declarative_base()


class EmployeeTable(Base):
    __tablename__ = 'employee_details'

    employee_id = Column(Integer, primary_key=True)
    employee_name = Column(String)
    salary = Column(Float)
    department = Column(String)
    contact_details = Column(BigInteger)
    gender = Column(String)
    employee_dob = Column(Date)
    employee_position = Column(String)
    user_name = Column(String)
    user_pass = Column(String)


class LoginTable(Base):
    __tablename__ = 'login_credentials'

    user_name = Column(String, primary_key=True)
    user_pass = Column(String)
    user_designation = Column(String)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    user_id = Column(String, nullable=True)  # Assuming user ID is a string
    action = Column(String, nullable=False)


class Token(BaseModel):
    access_token:str
    barear: str
