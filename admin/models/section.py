# admin/models/section.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from main.databases import Base, ToString


class Section(Base, ToString):
  __tablename__ = "sections"

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
    nullable=True
  )

  description = Column(
    Text,
    nullable=True
  )

  image_url = Column(
    String(100),
    nullable=True
  )

  course_id = Column(
    Integer,
    ForeignKey("courses.id", ondelete="CASCADE"),
    nullable=False
  )

  # Relationships
  course = relationship(
    "Course",
    back_populates="sections"
  )

  adverts = relationship(
    "Advert",
    back_populates="section"
  )

  worker_roles = relationship(
    "SectionWorkerRole",
    back_populates="section"
  )

  def __init__(
    self,
    name,
    course_id,
    code=None,
    description=None,
    image_url=None
  ):
    self.name = name
    self.course_id = course_id
    self.code = code
    self.description = description
    self.image_url = image_url

  def to_dict(self):
    return {
      "id": self.id,
      "name": self.name,
      "code": self.code,
      "description": self.description,
      "image_url": self.image_url,
      "course_id": self.course_id
    }