# admin/models/sex.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

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

  persons = relationship(
    "Person",
    back_populates="sex"
  )

  def __init__(self, name):
    self.name = name