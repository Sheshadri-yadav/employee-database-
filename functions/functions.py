from database.db import Session
from models.model import EmployeeTable, LoginTable
from datetime import date


class DatabaseError(Exception):
    pass


class AuthenticationError(Exception):
    pass


class EmployeeNotFoundError(Exception):
    pass


class EmployeeUpdateError(Exception):
    pass


def insert_employee_details(employee_details):
    try:
        with Session() as session:
            employee = EmployeeTable(
                employee_id=employee_details.id,
                employee_name=employee_details.name,
                salary=employee_details.salary,
                department=employee_details.dept,
                contact_details=employee_details.contact_number,
                gender=employee_details.gender,
                employee_dob=employee_details.dob,
                employee_position=employee_details.position,
                user_name=employee_details.user_name,
                user_pass=employee_details.user_pass
            )
            login = LoginTable(
                user_name=employee_details.user_name,
                user_pass=employee_details.user_pass,
                user_designation=employee_details.position
            )
            session.add(login)
            session.add(employee)
            session.commit()
            return "Employee data successfully inserted."
    except Exception as e:
        raise DatabaseError("Error occurred while inserting employee data: " + str(e))


def check_login(login_details):
    try:
        with Session() as session:
            user = session.query(LoginTable).filter(LoginTable.user_name == login_details.user_name,
                                                    LoginTable.user_pass == login_details.user_pass).first()
            if not user:
                raise AuthenticationError("Login Unsuccessful")
            user_position = user.user_designation if user else None
            if user_position not in ["admin"]:
                user_position = "employee"
            return True, "Login successful, redirecting to another page", user_position
    except Exception as e:
        raise DatabaseError("Error occurred during login: " + str(e))


def delete_employee(employee_id):
    try:
        with Session() as session:
            employee = session.query(EmployeeTable).filter(EmployeeTable.employee_id == employee_id).first()
            if not employee:
                raise EmployeeNotFoundError(f"No employee found with ID {employee_id}.")
            session.delete(employee)
            session.commit()
            return f"Employee with ID {employee_id} deleted successfully."
    except Exception as e:
        raise DatabaseError("Error occurred while deleting employee: " + str(e))


def update_employee(employee_id, name, salary, dept, contact_number, gender, dob, position):
    try:
        with Session() as session:
            employee = session.query(EmployeeTable).filter(EmployeeTable.employee_id == employee_id).first()
            if not employee:
                raise EmployeeNotFoundError(f"No employee found with ID {employee_id}.")
            employee.name = name
            employee.salary = salary
            employee.department = dept
            employee.contact_number = contact_number
            employee.gender = gender
            employee.dob = dob
            employee.position = position
            session.commit()
            return f"Employee with ID {employee_id} updated successfully."
    except Exception as e:
        raise EmployeeUpdateError("Error occurred while updating employee: " + str(e))


def display_currentUser(employee_id):
    try:
        with Session() as session:
            employee = session.query(EmployeeTable).filter(EmployeeTable.employee_id == employee_id).first()
            if not employee:
                raise EmployeeNotFoundError(f"No employee found with ID {employee_id}.")
            employee_info = {
                "employee_id": employee.employee_id,
                "employee_name": employee.employee_name,
                "salary": employee.salary,
                "department": employee.department,
                "contact_details": employee.contact_details,
                "gender": employee.gender,
                "dob": employee.employee_dob,
                "position": employee.employee_position,
                "user_name": employee.user_name,
                "user_pass": employee.user_pass
            }
            return employee_info
    except Exception as e:
        raise DatabaseError("Error occurred while fetching employee data: " + str(e))


def search_user(name):
    try:
        with Session() as session:
            search_results = session.query(EmployeeTable).filter(EmployeeTable.employee_name.ilike(f"%{name}%")).all()
            if not search_results:
                raise EmployeeNotFoundError(f"No employee found with name {name}.")
            return [
                {
                    "employee_id": result.employee_id,
                    "employee_name": result.employee_name,
                    "salary": result.salary,
                    "department": result.department,
                    "contact_details": result.contact_details,
                    "gender": result.gender,
                    "dob": result.employee_dob,
                    "position": result.employee_position,
                    "user_name": result.user_name,
                    "user_pass": result.user_pass
                }
                for result in search_results
            ]
    except Exception as e:
        raise DatabaseError("Error occurred while searching for employees: " + str(e))
