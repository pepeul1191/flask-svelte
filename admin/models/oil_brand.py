# admin/models/oil_brand.py

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from main.databases import Base, ToString


class OilBrand(Base, ToString):
  __tablename__ = "oil_brands"

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

  # Relación con oils activada
  oils = relationship(
    "Oil",
    back_populates="oil_brand",
    cascade="all, delete-orphan"
  )

  def __init__(self, name, description=None):
    self.name = name
    self.description = description

  def to_dict(self):
    return {
      "id": self.id,
      "name": self.name,
      "description": self.description
    }
