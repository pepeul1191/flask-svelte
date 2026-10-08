# admin/models/brand.py

from datetime import datetime
from sqlalchemy import Column, BigInteger, String, Text, DateTime
from sqlalchemy.orm import relationship
from main.databases import Base, ToString


class Brand(Base, ToString):
  __tablename__ = "brands"

  id = Column(
    BigInteger,
    primary_key=True,
    autoincrement=True
  )

  name = Column(
    String(100),
    unique=True,
    nullable=False
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

  # Relación preparada para la futura entidad BrandModel (tabla brand_models)
  """
  brand_models = relationship(
    "BrandModel",
    back_populates="brand",
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