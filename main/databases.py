# main/databases.py

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()


class ToString:

  def to_dict(self):
    return {
      key: value
      for key, value in self.__dict__.items()
      if not key.startswith("_")
    }

  def __repr__(self):
    attrs = ", ".join(
      f"{key}={value}"
      for key, value in self.__dict__.items()
      if not key.startswith("_")
    )
    return f"<{self.__class__.__name__}({attrs})>"


DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = (
  f"mysql+pymysql://"
  f"{DB_USER}:{DB_PASSWORD}"
  f"@{DB_HOST}:{DB_PORT}"
  f"/{DB_NAME}"
  f"?charset=utf8mb4"
)

engine = create_engine(
  DATABASE_URL,
  echo=True,
  pool_pre_ping=True
)

SessionLocal = sessionmaker(
  bind=engine,
  autocommit=False,
  autoflush=False
)

Base = declarative_base()


def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()