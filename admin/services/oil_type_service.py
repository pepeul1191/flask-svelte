# admin/services/oil_type_service.py

from sqlalchemy.exc import SQLAlchemyError

from admin.models.oil_type import OilType
from main.databases import SessionLocal
from main.services import ApplicationService


class OilTypeService(ApplicationService):

  @classmethod
  def fetch_all(cls, page=1, per_page=10, search_query=None):
    db = SessionLocal()

    try:
      query = db.query(OilType)

      # SEARCH
      if search_query:
        query = query.filter(
          OilType.name.ilike(f"%{search_query}%")
        )

      total_oil_types = query.count()

      oil_types = (
        query
        .order_by(OilType.id.asc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
      )

      total_pages = (
        (total_oil_types + per_page - 1) // per_page
      )

      start_record = (
        (page - 1) * per_page + 1
        if total_oil_types > 0
        else 0
      )

      end_record = min(
        page * per_page,
        total_oil_types
      )

      return cls.build_response(
        data={
          "oil_types": [
            oil_type.to_dict()
            for oil_type in oil_types
          ],
          "pagination": {
            "page": page,
            "per_page": per_page,
            "total_oil_types": total_oil_types,
            "total_pages": total_pages,
            "start_record": start_record,
            "end_record": end_record
          }
        },
        message="Lista de tipos de aceite obtenida exitosamente"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al obtener tipos de aceite: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def fetch_one(cls, oil_type_id):
    db = SessionLocal()

    try:
      oil_type = (
        db.query(OilType)
        .filter(OilType.id == oil_type_id)
        .first()
      )

      if not oil_type:
        return cls.handle_not_found(
          "Tipo de aceite no encontrado"
        )

      return cls.build_response(
        data=oil_type.to_dict(),
        message="Tipo de aceite encontrado"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al buscar tipo de aceite: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def create(cls, params):
    db = SessionLocal()

    try:
      oil_type = OilType(
        name=params.get("name"),
        description=params.get("description")
      )

      db.add(oil_type)
      db.commit()
      db.refresh(oil_type)

      return cls.build_response(
        data=oil_type.to_dict(),
        message="Tipo de aceite creado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al crear tipo de aceite: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def update(cls, oil_type_id, params):
    db = SessionLocal()

    try:
      oil_type = (
        db.query(OilType)
        .filter(OilType.id == oil_type_id)
        .first()
      )

      if not oil_type:
        return cls.handle_not_found(
          "Tipo de aceite no encontrado"
        )

      if "name" in params:
        oil_type.name = params["name"]

      if "description" in params:
        oil_type.description = params["description"]

      db.commit()
      db.refresh(oil_type)

      return cls.build_response(
        data=oil_type.to_dict(),
        message="Tipo de aceite actualizado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al actualizar tipo de aceite: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def delete(cls, oil_type_id):
    db = SessionLocal()

    try:
      oil_type = (
        db.query(OilType)
        .filter(OilType.id == oil_type_id)
        .first()
      )

      if not oil_type:
        return cls.handle_not_found(
          "Tipo de aceite no encontrado"
        )

      db.delete(oil_type)
      db.commit()

      return cls.build_response(
        message="Tipo de aceite eliminado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al eliminar tipo de aceite: {str(e)}"
      )

    finally:
      db.close()