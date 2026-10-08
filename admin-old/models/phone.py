# admin/models/phone.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from main.databases import Base, ToString


class Phone(Base, ToString):
  __tablename__ = "phones"

  id = Column(
    Integer,
    primary_key=True,
    autoincrement=True
  )

  person_id = Column(
    Integer,
    ForeignKey("persons.id"),
    nullable=False
  )

  description = Column(
    String(40),
    nullable=True
  )

  phone = Column(
    String(20),
    nullable=False
  )

  # Relaciones
  person = relationship(
    "Person",
    back_populates="phones"
  )

  def to_dict(self):
    return {
      "id": self.id,
      "person_id": self.person_id,
      "description": self.description,
      "phone": self.phone,
    }

  def __init__(
    self,
    person_id,
    phone,
    description=None
  ):
    self.person_id = person_id
    self.phone = phone
    self.description = description