
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
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task
    

def updateTodoList(task : str, request : schemas.UpdateToDo ,db : Session):
    todo = db.query(ToDo).filter(ToDo.title == task).first()
    if not todo:
        return {"Error":"Task not found"}
    todo.status = request.status
    db.commit()
    db.refresh(todo)
    return todo


def delete(task : str, db : Session):
    task = db.query(ToDo).filter(ToDo.title == task).first()
    if not task:
        return {"Error":"Task not found"}
    db.delete(task)
    db.commit()
    return task

