from pydantic import BaseModel
from typing import List

class ToDoBase(BaseModel):
    title : str
    status : bool

class CreateToDo(ToDoBase):
    pass

class UpdateToDo(ToDoBase):
    pass

class ToDo(ToDoBase):
    id : int


    class Config:
        orm_mode = True


    