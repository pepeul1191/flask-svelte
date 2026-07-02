# admin/models/student.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from main.databases import Base, ToString


class Student(Base, ToString):
  __tablename__ = "students"

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

  user_id = Column(
    Integer,
    ForeignKey("users.id"),
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
    back_populates="student"
  )

  representative_roles = relationship(
    "RepresentativeStudentRole",
    back_populates="student",
    cascade="all, delete-orphan"
  )

  def to_dict(self):
    return {
      "id": self.id,
      "code": self.code,
      "email": self.email,
      "user_id": self.user_id,
      "person_id": self.person_id,
      "person": self.person.to_dict() if self.person else None
    }

  def __init__(
    self,
    code,
    email,
    person_id,
    user_id=None
  ):
    self.code = code
    self.email = email
    self.person_id = person_id
    self.user_id = user_id