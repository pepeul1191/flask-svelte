# admin/models/address.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from main.databases import Base, ToString


class Address(Base, ToString):
  __tablename__ = "addresses"

  id = Column(
    Integer,
    primary_key=True,
    autoincrement=True
  )

  person_id = Column(
    Integer,
    ForeignKey("persons.id"),
    nullable=False
  )

  district_id = Column(
    Integer,
    ForeignKey("vw_locations.id"),
    nullable=False
  )

  description = Column(
    String(40),
    nullable=True
  )

  address = Column(
    String(255),
    nullable=False
  )

  # Relaciones
  person = relationship(
    "Person",
    back_populates="addresses"
  )

  district = relationship(
    "VwLocation",
    foreign_keys=[district_id]
  )

  def to_dict(self):
    return {
      "id": self.id,
      "person_id": self.person_id,
      "district_id": self.district_id,
      "description": self.description,
      "address": self.address,
      "district": self.district.to_dict() if self.district else None
    }

  def __init__(
    self,
    person_id,
    district_id,
    address,
    description=None
  ):
    self.person_id = person_id
    self.district_id = district_id
    self.address = address
    self.description = description