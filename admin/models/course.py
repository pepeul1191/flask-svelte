# admin/models/course.py

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from main.databases import Base, ToString


class Course(Base, ToString):
  __tablename__ = "courses"

  id = Column(
    Integer,
    primary_key=True,
    autoincrement=True
  )

  name = Column(
    String(45),
    nullable=False
  )

  code = Column(
    String(20),
    nullable=False
  )

  description = Column(
    Text,
    nullable=True
  )

  sylabus_url = Column(
    String(100),
    nullable=True
  )

  level_id = Column(
    Integer,
    ForeignKey("levels.id"),
    nullable=False
  )

  worker_id = Column(
    Integer,
    ForeignKey("workers.id"),
    nullable=True
  )

  # Relationships
  level = relationship(
    "Level",
    back_populates="courses"
  )

  worker = relationship(
    "Worker",
    back_populates="courses"
  )

  def __init__(self, name, code, level_id, description=None, sylabus_url=None, worker_id=None):
    self.name = name
    self.code = code
    self.level_id = level_id
    self.description = description
    self.sylabus_url = sylabus_url
    self.worker_id = worker_id

  def to_dict(self):
    return {
      "id": self.id,
      "name": self.name,
      "code": self.code,
      "description": self.description,
      "sylabus_url": self.sylabus_url,
      "level_id": self.level_id,
      "worker_id": self.worker_id
    }