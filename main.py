from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routes.route import manager, employee_details

app = FastAPI()

templates: Jinja2Templates = Jinja2Templates(directory="templates")
# Mount the directory containing your static files (HTML, CSS, JavaScript)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(manager)




#all are landing pages

@app.get("/")
async def loginPage(request: Request):
    return templates.TemplateResponse(
        "login.html", {"request": request}
    )


@app.post("/admin")
async def adminPage(request: Request):
    response = await employee_details()

    return templates.TemplateResponse(
        "admin.html", {"request": request, "response": response}
    )


@app.post("/employee")
async def EmployeePage(request: Request):
    response = await employee_details()
    print(response)
    return templates.TemplateResponse(
        "employee.html", {"request": request, "response": response}
    )


@app.get("/employee_details/updating/{employeeId}")
async def UpdateForm(request: Request):

    return templates.TemplateResponse(
        "UpdatingForm.html", {"request": request}
    )

@app.get("/addEmployee")
async def AddingNewEmployee(request:Request):
    return templates.TemplateResponse(
        "new_employee.html", {"request": request}
    )