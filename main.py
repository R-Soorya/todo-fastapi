from fastapi import FastAPI, Depends, Request
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
    return "Check Your To-Do list"
     

@app.get("/todo", response_model=List[schemas.ToDo])
async def getTodoList(request:Request, db : Session = Depends(get_db)):
    tasks = crud.getTodoList(db)
    if tasks is None:
        return []
    return tasks
   

@app.get("/todo/{id}", response_model=schemas.ToDo)
async def getToDoById(request:Request, id : int, db : Session = Depends(get_db)):
    task = crud.getTodoById(id, db)
    if task is None:
        return []
    return task


@app.post("/", response_model=schemas.ToDo)
async def create(request:schemas.CreateToDo, db:Session = Depends(get_db)):
    new_task = crud.createTodoList(request, db)
    return new_task


@app.put("/{task}", response_model = schemas.ToDo)
async def update(task:str, request:schemas.UpdateToDo ,db:Session = Depends(get_db)):
    todo = crud.updateTodoList(task, request, db)
    return todo


@app.delete("/{task}", response_model=schemas.ToDo)
async def delete(task:str, db:Session = Depends(get_db)):
    task = crud.delete(task, db)
    return task

