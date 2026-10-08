# admin/models/branch.py

from sqlalchemy import (
  Column,
  Integer,
  String
)
from sqlalchemy.orm import relationship

from main.databases import Base, ToString


class CourseBranch(Base, ToString):
  __tablename__ = "course_branches"

  id = Column(
    Integer,
    primary_key=True,
    autoincrement=True
  )

  name = Column(
    String(30),
    nullable=False
  )

  # Relación con Course
  courses = relationship(
    "Course",
    back_populates="course_branch"
  )

  def to_dict(self):
    return {
      "id": self.id,
      "name": self.name
    }

  def __init__(
    self,
    name,
  ):
    self.name = name