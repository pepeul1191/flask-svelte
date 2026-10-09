# admin/models/client.py

from datetime import datetime
from sqlalchemy import Column, BigInteger, String, Text, DateTime
from sqlalchemy.orm import relationship
from main.databases import Base, ToString


class Client(Base, ToString):
  __tablename__ = "clients"

  id = Column(
    BigInteger,
    primary_key=True,
    autoincrement=True
  )

  name = Column(
    String(150),
    nullable=False
  )

  contact_name = Column(
    String(150),
    nullable=False
  )

  email = Column(
    String(150),
    nullable=True
  )

  phone = Column(
    String(50),
    nullable=True
  )

  address = Column(
    Text,
    nullable=True
  )

  notes = Column(
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

  # Relación con ClientWorker (asociación jerárquica)
  client_workers = relationship(
    "ClientWorker",
    back_populates="client",
    cascade="all, delete-orphan"
  )

  def __init__(self, name, contact_name, email=None, phone=None, address=None, notes=None):
    self.name = name
    self.contact_name = contact_name
    self.email = email
    self.phone = phone
    self.address = address
    self.notes = notes

  def to_dict(self):
    return {
      "id": self.id,
      "name": self.name,
      "contact_name": self.contact_name,
      "email": self.email,
      "phone": self.phone,
      "address": self.address,
      "notes": self.notes,
      "created_at": self.created_at.isoformat() if self.created_at else None,
      "updated_at": self.updated_at.isoformat() if self.updated_at else None
    }