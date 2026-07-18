# admin/models/section_worker_role.py

from sqlalchemy import (
  Column,
  Integer,
  ForeignKey,
  UniqueConstraint
)
from sqlalchemy.orm import relationship

from main.databases import Base, ToString


class SectionWorkerRole(Base, ToString):
  __tablename__ = "sections_workers_roles"

  __table_args__ = (
    UniqueConstraint(
      "section_id",
      "worker_id",
      "worker_role_id",
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

  worker_id = Column(
    Integer,
    ForeignKey("workers.id"),
    nullable=False
  )

  worker_role_id = Column(
    Integer,
    ForeignKey("worker_roles.id"),
    nullable=False
  )

  section = relationship(
    "Section",
    back_populates="worker_roles"
  )

  worker = relationship(
    "Worker",
    back_populates="section_roles"
  )

  worker_role = relationship(
    "WorkerRole",
    back_populates="section_workers"
  )

  def to_dict(self):
    return {
      "id": self.id,
      "section_id": self.section_id,
      "worker_id": self.worker_id,
      "worker_role_id": self.worker_role_id,
      "section": (
        self.section.to_dict()
        if self.section else None
      ),
      "worker": (
        self.worker.to_dict()
        if self.worker else None
      ),
      "worker_role": (
        self.worker_role.to_dict()
        if self.worker_role else None
      )
    }

  def __init__(
    self,
    section_id,
    worker_id,
    worker_role_id
  ):
    self.section_id = section_id
    self.worker_id = worker_id
    self.worker_role_id = worker_role_id