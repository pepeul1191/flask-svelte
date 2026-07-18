# admin/models/worker.py

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from main.databases import Base, ToString


class Worker(Base, ToString):
  __tablename__ = "workers"

  id = Column(
    Integer,
    primary_key=True,
    autoincrement=True
  )

  code = Column(
    String(20),
    nullable=False,
    unique=True
  )

  email = Column(
    String(100),
    nullable=False
  )

  bio = Column(
    Text,
    nullable=True
  )

  person_id = Column(
    Integer,
    ForeignKey("persons.id"),
    nullable=False,
    unique=True
  )

  person = relationship(
    "Person",
    back_populates="worker"
  )

  # Agregar relación con courses
  courses = relationship(
    "Course",
    back_populates="worker"
  )

  adverts = relationship(
    "Advert",
    back_populates="worker"
  )

  def to_dict(self):
    return {
      "id": self.id,
      "code": self.code,
      "email": self.email,
      "bio": self.bio,
      "person_id": self.person_id,
      "person": self.person.to_dict() if self.person else None
    }

  def __init__(
    self,
    code,
    email,
    person_id,
    bio=None
  ):
    self.code = code
    self.email = email
    self.person_id = person_id
    self.bio = bio