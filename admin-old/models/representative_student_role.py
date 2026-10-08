# admin/models/representative_student_role.py

from sqlalchemy import (
  Column,
  Integer,
  ForeignKey,
  UniqueConstraint
)
from sqlalchemy.orm import relationship

from main.databases import Base, ToString


class RepresentativeStudentRole(Base, ToString):
  __tablename__ = "representatives_students_roles"

  __table_args__ = (
    UniqueConstraint(
      "representative_id",
      "student_id",
      "representative_role_id",
      name="uq_rsr_unique_combination"
    ),
  )

  id = Column(
    Integer,
    primary_key=True,
    autoincrement=True
  )

  representative_id = Column(
    Integer,
    ForeignKey("representatives.id"),
    nullable=False
  )

  student_id = Column(
    Integer,
    ForeignKey("students.id"),
    nullable=False
  )

  representative_role_id = Column(
    Integer,
    ForeignKey("representative_roles.id"),
    nullable=False
  )

  representative = relationship(
    "Representative",
    back_populates="student_roles"
  )

  student = relationship(
    "Student",
    back_populates="representative_roles"
  )

  representative_role = relationship(
    "RepresentativeRole",
    back_populates="representative_students"
  )

  def to_dict(self):
    return {
      "id": self.id,
      "representative_id": self.representative_id,
      "student_id": self.student_id,
      "representative_role_id": self.representative_role_id,
      "representative": self.representative.to_dict() if self.representative else None,
      "student": self.student.to_dict() if self.student else None,
      "representative_role": (
        self.representative_role.to_dict()
        if self.representative_role else None
      )
    }

  def __init__(
    self,
    representative_id,
    student_id,
    representative_role_id
  ):
    self.representative_id = representative_id
    self.student_id = student_id
    self.representative_role_id = representative_role_id