# admin/models/departament.py
from sqlalchemy import Column, Integer, String
from main.databases import Base, ToString

class Department(Base, ToString):
  __tablename__ = "departments"

  id = Column(
    Integer,
    primary_key=True,
    autoincrement=True
  )

  name = Column(
    String(45),
    nullable=False
  )

  def __init__(self, name):
    self.name = name