# admin/models/advert.py

from sqlalchemy import (
  Column,
  Integer,
  String,
  Text,
  Boolean,
  DateTime,
  ForeignKey
)
from sqlalchemy.orm import relationship

from main.databases import Base, ToString


class Advert(Base, ToString):
  __tablename__ = "adverts"

  id = Column(
    Integer,
    primary_key=True,
    autoincrement=True
  )

  header = Column(
    String(45),
    nullable=False
  )

  description = Column(
    Text,
    nullable=True
  )

  created = Column(
    DateTime,
    nullable=False
  )

  updated = Column(
    DateTime,
    nullable=False
  )

  published_from = Column(
    DateTime,
    nullable=True
  )

  published_to = Column(
    DateTime,
    nullable=True
  )

  visible = Column(
    Boolean,
    nullable=False,
    default=True
  )

  section_id = Column(
    Integer,
    ForeignKey("sections.id"),
    nullable=False
  )

  worker_id = Column(
    Integer,
    ForeignKey("workers.id"),
    nullable=False
  )

  section = relationship(
    "Section",
    back_populates="adverts"
  )

  worker = relationship(
    "Worker",
    back_populates="adverts"
  )

  def __init__(
    self,
    header,
    description,
    created,
    updated,
    published_from,
    published_to,
    visible,
    section_id,
    worker_id
  ):
    self.header = header
    self.description = description
    self.created = created
    self.updated = updated
    self.published_from = published_from
    self.published_to = published_to
    self.visible = visible
    self.section_id = section_id
    self.worker_id = worker_id

  def to_dict(self):
    return {
      "id": self.id,
      "header": self.header,
      "description": self.description,
      "created": self.created.isoformat() if self.created else None,
      "updated": self.updated.isoformat() if self.updated else None,
      "published_from": self.published_from.isoformat() if self.published_from else None,
      "published_to": self.published_to.isoformat() if self.published_to else None,
      "visible": self.visible,
      "section_id": self.section_id,
      "worker_id": self.worker_id,
      "section": self.section.to_dict() if self.section else None,
      "worker": self.worker.to_dict() if self.worker else None
    }