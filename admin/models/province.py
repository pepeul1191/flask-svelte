# admin/models/province.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from main.databases import Base, ToString


class Province(Base, ToString):
  __tablename__ = "provinces"

  id = Column(
    Integer,
    primary_key=True,
    autoincrement=True
  )

  name = Column(
    String(45),
    nullable=False
  )

  department_id = Column(
    Integer,
    ForeignKey("departments.id"),
    nullable=False
  )

  # (opcional pero recomendado)
  department = relationship("Department", backref="provinces")

  def __init__(self, name, department_id):
    self.name = name
    self.department_id = department_id