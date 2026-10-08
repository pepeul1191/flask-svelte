# admin/models/representative.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from main.databases import Base, ToString


class Representative(Base, ToString):
  __tablename__ = "representatives"

  id = Column(
    Integer,
    primary_key=True,
    autoincrement=True
  )

  email = Column(
    String(100),
    nullable=False
  )

  user_id = Column(
    Integer,
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
    back_populates="representative"
  )

  student_roles = relationship(
    "RepresentativeStudentRole",
    back_populates="representative",
    cascade="all, delete-orphan"
  )

  def to_dict(self):
    return {
      "id": self.id,
      "email": self.email,
      "user_id": self.user_id,
      "person_id": self.person_id,
      "person": self.person.to_dict() if self.person else None
    }

  def __init__(
    self,
    email,
    user_id,
    person_id
  ):
    self.email = email
    self.user_id = user_id
    self.person_id = person_id