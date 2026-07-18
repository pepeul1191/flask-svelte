# admin/models/branch.py

from sqlalchemy import (
  Column,
  Integer,
  String
)
from sqlalchemy.orm import relationship

from main.databases import Base, ToString


class Branch(Base, ToString):
  __tablename__ = "branches"

  id = Column(
    Integer,
    primary_key=True,
    autoincrement=True
  )

  name = Column(
    String(30),
    nullable=False
  )

  # Eliminar las columnas que no existen en la tabla
  # description = Column(Text, nullable=True)
  # is_active = Column(Boolean, default=True)
  # created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
  # updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

  # Relación con Course
  courses = relationship(
    "Course",
    back_populates="branch"
  )

  def to_dict(self):
    return {
      "id": self.id,
      "name": self.name
      # Eliminar los campos que no existen
      # "description": self.description,
      # "is_active": self.is_active,
      # "created_at": self.created_at.isoformat() if self.created_at else None,
      # "updated_at": self.updated_at.isoformat() if self.updated_at else None
    }

  def __init__(
    self,
    name,
    description=None,  # Mantener el parámetro pero no usarlo
    is_active=True      # Mantener el parámetro pero no usarlo
  ):
    self.name = name
    # self.description = description
    # self.is_active = is_active