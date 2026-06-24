# admin/models/sex.py
from sqlalchemy import Column, Integer, String
from main.databases import Base, ToString

class Sex(Base, ToString):
  __tablename__ = "sexs"

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