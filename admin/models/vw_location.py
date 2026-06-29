# admin/models/vw_location.py

from sqlalchemy import Column, Integer, String

from main.databases import Base, ToString


class VwLocation(Base, ToString):
  __tablename__ = "vw_locations"

  id = Column(
    Integer,
    primary_key=True
  )

  name = Column(
    String,
    nullable=False
  )

  def to_dict(self):
    return {
      "id": self.id,
      "name": self.name
    }