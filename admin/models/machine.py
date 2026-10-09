# admin/models/machine.py

from datetime import datetime
from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from main.databases import Base, ToString


class Machine(Base, ToString):
  __tablename__ = "machines"

  id = Column(
    BigInteger,
    primary_key=True,
    autoincrement=True
  )

  client_id = Column(
    BigInteger,
    ForeignKey("clients.id", ondelete="CASCADE"),
    nullable=False
  )

  model_id = Column(
    BigInteger,
    ForeignKey("brand_models.id", ondelete="RESTRICT"),
    nullable=False
  )

  name = Column(
    String(150),
    nullable=False
  )

  code = Column(
    String(100),
    unique=True,
    nullable=False
  )

  serial_number = Column(
    String(100),
    unique=True,
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

  # Relaciones
  client = relationship(
    "Client",
    backref="machines"
  )

  brand_model = relationship(
    "BrandModel",
    backref="machines"
  )

  def __init__(
    self,
    client_id,
    model_id,
    name,
    code,
    serial_number=None
  ):
    self.client_id = client_id
    self.model_id = model_id
    self.name = name
    self.code = code
    self.serial_number = serial_number

  def to_dict(self):
    return {
      "id": self.id,
      "client_id": self.client_id,
      "model_id": self.model_id,
      "name": self.name,
      "code": self.code,
      "serial_number": self.serial_number,
      "created_at": self.created_at.isoformat() if self.created_at else None,
      "updated_at": self.updated_at.isoformat() if self.updated_at else None
    }