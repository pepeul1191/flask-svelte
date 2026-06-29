# admin/services/district_service.py

from sqlalchemy.exc import SQLAlchemyError

from admin.models.district import District
from admin.models.vw_location import VwLocation
from main.databases import SessionLocal
from main.services import ApplicationService


class DistrictService(ApplicationService):

  @classmethod
  def fetch_by_province(cls, province_id):
    db = SessionLocal()

    try:
      districts = (
        db.query(District)
        .filter(District.province_id == province_id)
        .order_by(District.id.asc())
        .all()
      )

      return cls.build_response(
        data=[d.to_dict() for d in districts],
        message="Distritos obtenidos correctamente"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al obtener distritos: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def create(cls, params):
    db = SessionLocal()

    try:
      district = District(
        name=params.get("name"),
        province_id=params.get("province_id")
      )

      db.add(district)
      db.commit()
      db.refresh(district)

      return cls.build_response(
        data=district.to_dict(),
        message="Distrito creado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al crear distrito: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def delete(cls, district_id):
    db = SessionLocal()

    try:
      district = (
        db.query(District)
        .filter(District.id == district_id)
        .first()
      )

      if not district:
        return cls.handle_not_found(
          "Distrito no encontrado"
        )

      db.delete(district)
      db.commit()

      return cls.build_response(
        message="Distrito eliminado"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al eliminar distrito: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def fetch_one(cls, district_id):
    db = SessionLocal()

    try:
      district = (
        db.query(District)
        .filter(District.id == district_id)
        .first()
      )

      if not district:
        return cls.handle_not_found(
          "Distrito no encontrado"
        )

      return cls.build_response(
        data=district.to_dict(),
        message="Distrito encontrado"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def update(cls, district_id, params):
    db = SessionLocal()

    try:
      district = (
        db.query(District)
        .filter(District.id == district_id)
        .first()
      )

      if not district:
        return cls.handle_not_found(
          "Distrito no encontrado"
        )

      if "name" in params:
        district.name = params["name"]

      if "province_id" in params:
        district.province_id = params["province_id"]

      db.commit()
      db.refresh(district)

      return cls.build_response(
        data=district.to_dict(),
        message="Distrito actualizado"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def search_by_name(cls, name):
    """Busca ubicaciones por nombre usando LIKE contra la vista"""
    db = SessionLocal()

    try:
      # Búsqueda case-insensitive con LIKE
      search_pattern = f"%{name}%"
      locations = (
        db.query(VwLocation)
        .filter(VwLocation.name.ilike(search_pattern))  # ilike = case-insensitive LIKE
        .order_by(VwLocation.name.asc())
        .limit(10)  # Límite para evitar sobrecarga
        .all()
      )

      return cls.build_response(
        data=[loc.to_dict() for loc in locations],
        message="Ubicaciones encontradas",
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al buscar ubicaciones: {str(e)}"
      )

    finally:
      db.close()