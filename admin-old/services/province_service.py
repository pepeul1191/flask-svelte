# admin/services/province_service.py
from sqlalchemy.exc import SQLAlchemyError

from admin.models.province import Province
from main.databases import SessionLocal
from main.services import ApplicationService


class ProvinceService(ApplicationService):

  @classmethod
  def fetch_by_department(cls, department_id):
    db = SessionLocal()

    try:
      provinces = (
        db.query(Province)
        .filter(Province.department_id == department_id)
        .order_by(Province.id.asc())
        .all()
      )

      return cls.build_response(
        data=[p.to_dict() for p in provinces],
        message="Provincias obtenidas correctamente"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al obtener provincias: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def create(cls, params):
    db = SessionLocal()

    try:
      province = Province(
        name=params.get("name"),
        department_id=params.get("department_id")
      )

      db.add(province)
      db.commit()
      db.refresh(province)

      return cls.build_response(
        data=province.to_dict(),
        message="Provincia creada exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al crear provincia: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def delete(cls, province_id):
    db = SessionLocal()

    try:
      province = (
        db.query(Province)
        .filter(Province.id == province_id)
        .first()
      )

      if not province:
        return cls.handle_not_found("Provincia no encontrada")

      db.delete(province)
      db.commit()

      return cls.build_response(
        message="Provincia eliminada"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al eliminar provincia: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def fetch_one(cls, province_id):
    db = SessionLocal()

    try:
      province = (
        db.query(Province)
        .filter(Province.id == province_id)
        .first()
      )

      if not province:
        return cls.handle_not_found("Provincia no encontrada")

      return cls.build_response(
        data=province.to_dict(),
        message="Provincia encontrada"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(f"Error: {str(e)}")

    finally:
      db.close()

  @classmethod
  def update(cls, province_id, params):
    db = SessionLocal()

    try:
      province = (
        db.query(Province)
        .filter(Province.id == province_id)
        .first()
      )

      if not province:
        return cls.handle_not_found("Provincia no encontrada")

      if "name" in params:
        province.name = params["name"]

      if "department_id" in params:
        province.department_id = params["department_id"]

      db.commit()
      db.refresh(province)

      return cls.build_response(
        data=province.to_dict(),
        message="Provincia actualizada"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(f"Error: {str(e)}")

    finally:
      db.close()