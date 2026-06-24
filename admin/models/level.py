# admin/models/level.py

from sqlalchemy import Column, Integer, String
from main.databases import Base, ToString


class Level(Base, ToString):
  __tablename__ = "levels"

  id = Column(
    Integer,
    primary_key=True,
    autoincrement=True
  )

  name = Column(
    String(30),
    nullable=False
  )

  def __init__(self, name):
    self.name = name