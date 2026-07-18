# admin/models/worker_role.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from main.databases import Base, ToString


class WorkerRole(Base, ToString):
  __tablename__ = "worker_roles"

  id = Column(
    Integer,
    primary_key=True,
    autoincrement=True
  )

  name = Column(
    String(40),
    nullable=False
  )

  section_workers = relationship(
    "SectionWorkerRole",
    back_populates="worker_role"
  )

  def __init__(
    self,
    name
  ):
    self.name = name

  def to_dict(self):
    return {
      "id": self.id,
      "name": self.name
    }