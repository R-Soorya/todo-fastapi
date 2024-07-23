from sqlalchemy import Column, String, Integer, Boolean
from database import Base

class ToDo(Base):
    __tablename__ = 'ToDo'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    status = Column(String, default=False)