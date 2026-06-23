# admin/models/district.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from main.databases import Base, ToString


class District(Base, ToString):
  __tablename__ = "districts"

  id = Column(
    Integer,
    primary_key=True,
    autoincrement=True
  )

  name = Column(
    String(45),
    nullable=False
  )

  province_id = Column(
    Integer,
    ForeignKey("provinces.id"),
    nullable=False
  )

  province = relationship(
    "Province",
    back_populates="districts"
  )

  def __init__(self, name, province_id):
    self.name = name
    self.province_id = province_id