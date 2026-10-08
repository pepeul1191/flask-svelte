# admin/models/level.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
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

  # Relación con courses
  courses = relationship(
    "Course",
    back_populates="level",
    cascade="all, delete-orphan"
  )

  def __init__(self, name):
    self.name = name

  def to_dict(self):
    return {
      "id": self.id,
      "name": self.name
    }