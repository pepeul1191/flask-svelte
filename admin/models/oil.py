# admin/models/oil.py

from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from main.databases import Base, ToString


class Oil(Base, ToString):
  __tablename__ = "oils"

  id = Column(
    Integer,
    primary_key=True,
    autoincrement=True
  )

  oil_brand_id = Column(
    Integer,
    ForeignKey("oil_brands.id", ondelete="CASCADE"),
    nullable=False
  )

  oil_type_id = Column(
    Integer,
    ForeignKey("oil_types.id", ondelete="CASCADE"),
    nullable=False
  )

  name = Column(
    String(150),
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

  # Relaciones hacia los modelos padre
  oil_brand = relationship(
    "OilBrand",
    back_populates="oils"
  )

  oil_type = relationship(
    "OilType",
    back_populates="oils"
  )

  def __init__(self, oil_brand_id, oil_type_id, name, description=None):
    self.oil_brand_id = oil_brand_id
    self.oil_type_id = oil_type_id
    self.name = name
    self.description = description

  def to_dict(self):
    return {
      "id": self.id,
      "oil_brand_id": self.oil_brand_id,
      "oil_type_id": self.oil_type_id,
      "name": self.name,
      "description": self.description,
      # Opcional: incluir los objetos serializados si lo necesitas en la API
      "oil_brand": self.oil_brand.to_dict() if self.oil_brand else None,
      "oil_type": self.oil_type.to_dict() if self.oil_type else None,
      "created_at": self.created_at.isoformat() if self.created_at else None,
      "updated_at": self.updated_at.isoformat() if self.updated_at else None
    }