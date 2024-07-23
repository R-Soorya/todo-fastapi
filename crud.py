
from sqlalchemy.orm import Session
import schemas
from models import ToDo


def getTodoList(db : Session):
    task =  db.query(ToDo).all()
    return task


def getTodoById(id, db : Session):
    task = db.query(ToDo).filter(ToDo.id == id).first()
    return task


def createTodoList(request : schemas.CreateToDo, db : Session):
    new_task = ToDo(title = request.title, status = request.status)
    tasks = getTodoList(db)
    tasks = [task.title for task in tasks]
    if new_task.title in tasks:
        new_task = None
        return
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task
    

def updateTodoList(status, task_id ,db : Session):
    todo = db.query(ToDo).filter(ToDo.id == task_id).first()
    todo.status = status
    db.commit()
    db.refresh(todo)
    return todo


def delete(task_id : int, db : Session):
    task = db.query(ToDo).filter(ToDo.id == task_id).first()
    if not task:
        return {"Error":"Task not found"}
    db.delete(task)
    db.commit()

