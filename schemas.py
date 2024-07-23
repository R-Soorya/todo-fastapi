from pydantic import BaseModel
from typing import List

class ToDoBase(BaseModel):
    title : str
    status : str

class CreateToDo(ToDoBase):
    pass

class UpdateToDo(BaseModel):
    status : str

class ToDo(ToDoBase):
    id : int


    class Config:
        orm_mode = True


    