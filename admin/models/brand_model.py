# admin/models/brand_model.py

from datetime import datetime
from sqlalchemy import Column, BigInteger, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from main.databases import Base, ToString


class BrandModel(Base, ToString):
  __tablename__ = "brand_models"

  id = Column(
    BigInteger,
    primary_key=True,
    autoincrement=True
  )

  brand_id = Column(
    BigInteger,
    ForeignKey("brands.id", ondelete="CASCADE"),
    nullable=False
  )

  name = Column(
    String(100),
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

  # Relación inversa con el modelo Brand
  brand = relationship(
    "Brand",
    back_populates="brand_models"
  )

  def __init__(self, brand_id, name, description=None):
    self.brand_id = brand_id
    self.name = name
    self.description = description

  def to_dict(self):
    return {
      "id": self.id,
      "brand_id": self.brand_id,
      "brand": self.brand.to_dict() if self.brand else None,
      "name": self.name,
      "description": self.description,
      "created_at": self.created_at.isoformat() if self.created_at else None,
      "updated_at": self.updated_at.isoformat() if self.updated_at else None
    }