# admin/models/section_student.py

from sqlalchemy import (
  Column,
  Integer,
  ForeignKey,
  UniqueConstraint
)
from sqlalchemy.orm import relationship

from main.databases import Base, ToString


class SectionStudent(Base, ToString):
  __tablename__ = "sections_students"

  __table_args__ = (
    UniqueConstraint(
      "section_id",
      "student_id",
      name="uq_swr_unique_combination"
    ),
  )

  id = Column(
    Integer,
    primary_key=True,
    autoincrement=True
  )

  section_id = Column(
    Integer,
    ForeignKey("sections.id"),
    nullable=False
  )

  student_id = Column(
    Integer,
    ForeignKey("students.id"),
    nullable=False
  )

  section = relationship(
    "Section",
    back_populates="students"
  )

  student = relationship(
    "Student",
    back_populates="sections"
  )

  def to_dict(self):
    return {
      "id": self.id,
      "section_id": self.section_id,
      "student_id": self.student_id,
      "section": (
        self.section.to_dict()
        if self.section else None
      ),
      "student": (
        self.student.to_dict()
        if self.student else None
      )
    }

  def __init__(
    self,
    section_id,
    student_id
  ):
    self.section_id = section_id
    self.student_id = student_id