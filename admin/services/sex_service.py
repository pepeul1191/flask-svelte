# admin/services/sex_service.py

from sqlalchemy.exc import SQLAlchemyError

from admin.models.sex import Sex
from main.databases import SessionLocal
from main.services import ApplicationService


class SexService(ApplicationService):

  @classmethod
  def fetch_all(cls):
    db = SessionLocal()

    try:
      sexes = (
        db.query(Sex)
        .order_by(Sex.id.asc())
        .all()
      )

      return cls.build_response(
        data=[sex.to_dict() for sex in sexes],
        message="Lista de sexos obtenida exitosamente"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al obtener los sexos: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def fetch_one(cls, sex_id):
    db = SessionLocal()

    try:
      sex = (
        db.query(Sex)
        .filter(Sex.id == sex_id)
        .first()
      )

      if not sex:
        return cls.handle_not_found(
          "Sexo no encontrado"
        )

      return cls.build_response(
        data=sex.to_dict(),
        message="Sexo encontrado"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al buscar el sexo: {str(e)}"
      )

    finally:
      db.close()