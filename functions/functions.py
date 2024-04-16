from database.db import Session
from models.model import EmployeeTable, EmployeeDetails, LoginTable, UserCredentials
from datetime import date


def insert_employee_details(employee_details: EmployeeDetails):
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
            print("Employee data successfully inserted.")
    except Exception as e:
        print("Error occurred while inserting employee data:", e)


employee_data = EmployeeDetails(
    id='admin123',
    name='sheshadri',
    salary=900000,
    dept='frontend',
    contact_number=7892693055,
    gender='Male',
    dob=date(2002, 6, 3),
    position='admin',
    user_name='admin',
    user_pass='admin'
)


# insert_employee_details(employee_data)


def check_login(login_details: UserCredentials):
    flag = 0
    with Session() as session:
        user = session.query(LoginTable).filter(LoginTable.user_name == login_details.user_name,
                                                LoginTable.user_pass == login_details.user_pass).first()
        if user:
            flag = 1
        message = "Login Unsuccessful" if flag == 0 else "Login successful, redirecting to another page"
        user_position = user.user_designation if user else None  # Assuming user has a field employee_position
        if user_position not in ["admin"]:
            user_position = "employee"
        print(user_position)
        return flag, message, user_position


log = UserCredentials(
    user_name='alice_smith',
    user_pass='securepassword'
)


# check_login(log)

def show_all_employees():
    with Session() as session:
        list1 = []
        all_users = session.query(EmployeeTable).all()
        for result in all_users:
            employee_info = {
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
            list1.append(employee_info)
        return list1


def delete_employee(employee_id: str):
    with Session() as session:
        employee = session.query(EmployeeTable).filter(EmployeeTable.employee_id == employee_id).first()
        if employee:
            session.delete(employee)
            session.commit()
            print(f"Employee with ID {employee_id} deleted successfully.")
        else:
            print(f"No employee found with ID {employee_id}.")


def update_employee(employee_id, name, salary, dept, contact_number, gender, dob, position):
    # Create a session
    with Session() as session:
        employee = session.query(EmployeeTable).filter(EmployeeTable.employee_id == employee_id).first()
        if employee:
            employee.name = name
            employee.salary = salary
            employee.department = dept
            employee.contact_number = contact_number
            employee.gender = gender
            employee.dob = dob
            employee.position = position
            session.commit()
            print(f"Employee with ID {employee_id} updated successfully.")
        else:
            print(f"No employee found with ID {employee_id}.")


"""


employee_id_to_update = "af323t12"  # Replace with the employee ID you want to update
update_employee(
    employee_id_to_update,
    name='Sheshu',
    salary=630000,
    dept='Engineering',
    contact_number='9876343210',
    gender='Male',
    dob=date(2001, 8, 25),
    position='Software Engineer'
)

"""


def display_currentUser(employee_id: str):
    with Session() as session:
        list1 = []
        employee = session.query(EmployeeTable).filter(EmployeeTable.employee_id == employee_id)
        for result in employee:
            employee_info = {
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
            list1.append(employee_info)
        return list1


def search_user(name: str):
    with Session() as session:
        list1 = []
        search = session.query(EmployeeTable).filter(EmployeeTable.employee_name.ilike(f"%{name}%")).all()
        for result in search:
            employee_info = {
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
            list1.append(employee_info)
        return list1
