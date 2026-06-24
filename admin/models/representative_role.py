# admin/models/representative_role.py

from sqlalchemy import Column, Integer, String
from main.databases import Base, ToString


class RepresentativeRole(Base, ToString):
  __tablename__ = "representative_roles"

  id = Column(
    Integer,
    primary_key=True,
    autoincrement=True
  )

  name = Column(
    String(20),
    nullable=False
  )

  def __init__(self, name):
    self.name = name