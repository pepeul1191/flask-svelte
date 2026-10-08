# admin/models/oil_type.py

from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship
from main.databases import Base, ToString


class OilType(Base, ToString):
  __tablename__ = "oil_types"

  id = Column(
    Integer,
    primary_key=True,
    autoincrement=True
  )

  name = Column(
    String(100),
    nullable=False,
    unique=True
  )

  description = Column(
    Text,
    nullable=True
  )

  created_at = Column(
    DateTime,
    default=datetime.utcnow,
    nullable=False
  )

  updated_at = Column(
    DateTime,
    default=datetime.utcnow,
    onupdate=datetime.utcnow,
    nullable=False
  )

  # Si en el futuro necesitas relacionarlo con otra entidad (ej. aceites), 
  # puedes descomentar y ajustar algo similar a esto:
  """
  oils = relationship(
    "Oil",
    back_populates="oil_type",
    cascade="all, delete-orphan"
  )
  """

  def __init__(self, name, description=None):
    self.name = name
    self.description = description

  def to_dict(self):
    return {
      "id": self.id,
      "name": self.name,
      "description": self.description,
      "created_at": self.created_at.isoformat() if self.created_at else None,
      "updated_at": self.updated_at.isoformat() if self.updated_at else None
    }