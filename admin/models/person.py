# admin/models/person.py

from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from main.databases import Base, ToString


class Person(Base, ToString):
  __tablename__ = "persons"

  id = Column(
    Integer,
    primary_key=True,
    autoincrement=True
  )

  names = Column(String(45), nullable=False)
  last_names = Column(String(45), nullable=False)

  document_number = Column(String(12), nullable=False)

  image_url = Column(String(70), nullable=True)

  birth_date = Column(Date, nullable=True)

  created = Column(DateTime, default=datetime.now, nullable=False)
  updated = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

  sex_id = Column(Integer, ForeignKey("sexs.id"), nullable=False)
  document_type_id = Column(Integer, ForeignKey("document_types.id"), nullable=False)

  sex = relationship(
    "Sex",
    back_populates="persons"
  )

  document_type = relationship(
    "DocumentType",
    back_populates="persons"
  )

  worker = relationship(
    "Worker",
    back_populates="person",
    uselist=False
  )

  # 👇 Agregar relación con teléfonos
  phones = relationship(
    "Phone",
    back_populates="person",
    cascade="all, delete-orphan"  # Elimina teléfonos cuando se elimina la persona
  )

  # Agregar al final de las relaciones:
  addresses = relationship(
    "Address",
    back_populates="person",
    cascade="all, delete-orphan"
  )

  def to_dict(self):
    return {
      "id": self.id,
      "names": self.names,
      "last_names": self.last_names,
      "document_number": self.document_number,
      "image_url": self.image_url,
      "birth_date": self.birth_date.isoformat() if self.birth_date else None,
      "created": self.created.isoformat() if self.created else None,
      "updated": self.updated.isoformat() if self.updated else None,
      "sex_id": self.sex_id,
      "document_type_id": self.document_type_id,
      "document_type": {
        "id": self.document_type.id,
        "name": self.document_type.name
      } if self.document_type else None,
      # 👇 Agregar teléfonos
      "phones": [p.to_dict() for p in self.phones] if self.phones else [],
      "addresses": [a.to_dict() for a in self.addresses] if self.addresses else []
    }
  
  def __init__(
    self,
    names,
    last_names,
    document_number,
    image_url,
    birth_date,
    sex_id,
    document_type_id
  ):
    self.names = names
    self.last_names = last_names
    self.document_number = document_number
    self.image_url = image_url
    self.birth_date = birth_date
    self.sex_id = sex_id
    self.document_type_id = document_type_id