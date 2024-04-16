from fastapi import APIRouter, Form, Request, HTTPException, Body, Depends, Header
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from functions import Oauth
from functions.functions import check_login, show_all_employees, display_currentUser, insert_employee_details, \
    delete_employee, update_employee, search_user
from models.model import UserCredentials, EmployeeDetails

manager = APIRouter()

templates = Jinja2Templates(directory="templates")



@manager.post("/login_page")
async def UserLogin(user_credentials: OAuth2PasswordRequestForm = Depends()):
    UserDetails = UserCredentials(user_name=user_credentials.username, user_pass=user_credentials.password)
    flag, message, user_position = check_login(UserDetails)

    if flag == 0:
        # Invalid username or password
        raise HTTPException(status_code=401, detail="Invalid username or password")

    elif flag == 1:
        if user_position == "admin":
            # Create access token
            access_token = Oauth.create_access_token(data={"user_position": user_position})
            print(access_token)
            return RedirectResponse(url="/admin", status_code=307)

        elif user_position == "employee":
            return RedirectResponse(url="/employee", status_code=307)

    else:
        raise HTTPException(status_code=500, detail="Invalid flag value")

@manager.get("/employee_details")
async def employee_details():
    try:
        all_employees = show_all_employees()
        return all_employees

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@manager.get("/employee_details/{employee_id}")
async def CurrentEmployee(employee_id: str, request: Request):
    try:
        response = display_currentUser(employee_id)
        return templates.TemplateResponse(
            "currentUser.html", {"request": request, "response": response}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@manager.post("/add_employee")
async def addEmployee(details: EmployeeDetails):
    try:
        insert_employee_details(details)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@manager.put("/employee_details/update/{employee_id}")
async def UpdateDetails(employee_id: str, details: EmployeeDetails):
    try:
        update_employee(employee_id, details.name, details.salary, details.dept, details.contact_number,
                        details.gender, details.dob, details.position)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@manager.delete("/delete_employee/{employee_id}")
async def DeleteData(
    employee_id: str
):
    try:
        # Delete employee if user is authorized
        delete_employee(employee_id)
        return {"success": True}
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=500, detail=str(e))
    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise e


@manager.get("/search")
async def SearchEmployee(request: Request):
    data = await request.json()
    user_name = data.get("name")
    user=search_user(user_name)
    return user