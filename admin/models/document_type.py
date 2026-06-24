# admin/models/document_type.py

from sqlalchemy import Column, Integer, String
from main.databases import Base, ToString


class DocumentType(Base, ToString):
  __tablename__ = "document_types"

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