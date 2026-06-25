# admin/models/worker.py
from sqlalchemy import Column, Integer, String, ForeignKey
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

  def to_dict(self):
    return {
      "id": self.id,
      "code": self.code,
      "email": self.email,
      "person_id": self.person_id,
      "person": self.person.to_dict() if self.person else None
    }

  def __init__(
    self,
    code,
    email,
    person_id
  ):
    self.code = code
    self.email = email
    self.person_id = person_id