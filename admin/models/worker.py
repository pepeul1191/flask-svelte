# admin/models/worker.py

from datetime import datetime
from sqlalchemy import Column, BigInteger, String, DateTime
from main.databases import Base, ToString


class Worker(Base, ToString):
  __tablename__ = "workers"

  id = Column(
    BigInteger,
    primary_key=True,
    autoincrement=True
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

  def __init__(self, names, last_names, email, user_id=None, document=None, phone=None, certification=None, position=None):
    self.user_id = user_id
    self.names = names
    self.last_names = last_names
    self.email = email
    self.document = document
    self.phone = phone
    self.certification = certification
    self.position = position

  @property
  def full_name(self):
    return f"{self.names} {self.last_names}"

  def to_dict(self):
    return {
      "id": self.id,
      "user_id": self.user_id,
      "names": self.names,
      "last_names": self.last_names,
      "full_name": self.full_name,
      "email": self.email,
      "document": self.document,
      "phone": self.phone,
      "certification": self.certification,
      "position": self.position,
      "created_at": self.created_at.isoformat() if self.created_at else None,
      "updated_at": self.updated_at.isoformat() if self.updated_at else None
    }