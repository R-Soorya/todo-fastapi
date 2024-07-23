from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import schemas, crud, models
from database import SessionLocal, engine
from typing import List

template = Jinja2Templates(directory="templates")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
async def home(request : Request):
    # return "Check Your To-Do list"
    return template.TemplateResponse("home.html", context={'request':request})
     

@app.post("/todo", response_class= HTMLResponse)
async def getTodoList(request:Request, db : Session = Depends(get_db)):
    tasks = crud.getTodoList(db)
    return template.TemplateResponse("todo.html", context={'request':request, 'tasks':tasks})
   

@app.post("/todo-by-id", response_class= HTMLResponse)
async def getToDoById(request:Request, id: int = Form(...), db : Session = Depends(get_db)):
    task = crud.getTodoById(id, db)
    if task is None:
        return template.TemplateResponse("todobyid.html", context={"request":request, "no_task":"No tasks for this ID"})
    return template.TemplateResponse("todobyid.html", context={"request":request, "task":task})

# ------------------Create-----------------------
@app.post("/create", response_class= HTMLResponse)
async def create(request:Request, title: str = Form(...), status: str = Form(...), db:Session = Depends(get_db)):
    new_task = schemas.CreateToDo(title=title, status=status)
    task = crud.createTodoList(new_task, db)
    if task == None:
        tasks = crud.getTodoList(db)
        return template.TemplateResponse("todo.html", context={'request':request, 'tasks':tasks, 'task':'Task exists'})
    response = RedirectResponse(url='/todo')
    return response

# ------------------Update-----------------------
@app.post("/update", response_class= HTMLResponse)
async def update(request:Request, task_id:str = Form(...) , status: str = Form(...), db:Session = Depends(get_db)):
    crud.updateTodoList(status, task_id, db)
    response = RedirectResponse(url='/todo')
    return response

# ------------------Delete-----------------------
@app.post("/delete", response_class=HTMLResponse)
async def delete(request: Request, task_id: str = Form(...), db:Session = Depends(get_db)):
    crud.delete(int(task_id), db)
    response = RedirectResponse(url="/todo")
    return response

