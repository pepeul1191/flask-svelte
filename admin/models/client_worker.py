# admin/models/client_worker.py

from datetime import datetime
from sqlalchemy import Column, BigInteger, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from main.databases import Base, ToString


class ClientWorker(Base, ToString):
  __tablename__ = "client_workers"

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

  user_id = Column(
    BigInteger,
    unique=True,
    nullable=True
  )

  names = Column(
    String(150),
    nullable=False
  )

  last_names = Column(
    String(150),
    nullable=False
  )

  email = Column(
    String(150),
    unique=True,
    nullable=False
  )

  document = Column(
    String(50),
    nullable=True
  )

  phone = Column(
    String(50),
    nullable=True
  )

  certification = Column(
    String(255),
    nullable=True
  )

  position = Column(
    String(100),
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

  # Relación con Client
  client = relationship(
    "Client",
    back_populates="client_workers"
  )

  def __init__(
    self,
    client_id,
    names,
    last_names,
    email,
    user_id=None,
    document=None,
    phone=None,
    certification=None,
    position=None
  ):
    self.client_id = client_id
    self.names = names
    self.last_names = last_names
    self.email = email
    self.user_id = user_id
    self.document = document
    self.phone = phone
    self.certification = certification
    self.position = position

  def to_dict(self):
    return {
      "id": self.id,
      "client_id": self.client_id,
      "user_id": self.user_id,
      "names": self.names,
      "last_names": self.last_names,
      "email": self.email,
      "document": self.document,
      "phone": self.phone,
      "certification": self.certification,
      "position": self.position,
      "created_at": self.created_at.isoformat() if self.created_at else None,
      "updated_at": self.updated_at.isoformat() if self.updated_at else None
    }