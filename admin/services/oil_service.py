# admin/services/oil_service.py

from sqlalchemy.exc import SQLAlchemyError

from admin.models.oil import Oil
from main.databases import SessionLocal
from main.services import ApplicationService


class OilService(ApplicationService):

  @classmethod
  def fetch_all(cls, page=1, per_page=10, search_query=None, oil_brand_id=None, oil_type_id=None):
    db = SessionLocal()

    try:
      query = db.query(Oil)

      # SEARCH POR NOMBRE (OPCIONAL)
      if search_query:
        query = query.filter(
          Oil.name.ilike(f"%{search_query}%")
        )

      # FILTRO OPCIONAL POR MARCA
      if oil_brand_id:
        query = query.filter(
          Oil.oil_brand_id == oil_brand_id
        )

      # FILTRO OPCIONAL POR TIPO
      if oil_type_id:
        query = query.filter(
          Oil.oil_type_id == oil_type_id
        )

      total_oils = query.count()

      oils = (
        query
        .order_by(Oil.id.asc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
      )

      total_pages = (
        (total_oils + per_page - 1) // per_page
      )

      start_record = (
        (page - 1) * per_page + 1
        if total_oils > 0
        else 0
      )

      end_record = min(
        page * per_page,
        total_oils
      )

      return cls.build_response(
        data={
          "oils": [
            oil.to_dict()
            for oil in oils
          ],
          "pagination": {
            "page": page,
            "per_page": per_page,
            "total_oils": total_oils,
            "total_pages": total_pages,
            "start_record": start_record,
            "end_record": end_record
          }
        },
        message="Lista de aceites obtenida exitosamente"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al obtener aceites: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def fetch_one(cls, oil_id):
    db = SessionLocal()

    try:
      oil = (
        db.query(Oil)
        .filter(Oil.id == oil_id)
        .first()
      )

      if not oil:
        return cls.handle_not_found(
          "Aceite no encontrado"
        )

      return cls.build_response(
        data=oil.to_dict(),
        message="Aceite encontrado"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al buscar aceite: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def create(cls, params):
    db = SessionLocal()

    try:
      oil = Oil(
        oil_brand_id=params.get("oil_brand_id"),
        oil_type_id=params.get("oil_type_id"),
        name=params.get("name"),
        description=params.get("description")
      )

      db.add(oil)
      db.commit()
      db.refresh(oil)

      return cls.build_response(
        data=oil.to_dict(),
        message="Aceite creado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al crear aceite: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def update(cls, oil_id, params):
    db = SessionLocal()

    try:
      oil = (
        db.query(Oil)
        .filter(Oil.id == oil_id)
        .first()
      )

      if not oil:
        return cls.handle_not_found(
          "Aceite no encontrado"
        )

      if "oil_brand_id" in params:
        oil.oil_brand_id = params["oil_brand_id"]

      if "oil_type_id" in params:
        oil.oil_type_id = params["oil_type_id"]

      if "name" in params:
        oil.name = params["name"]

      if "description" in params:
        oil.description = params["description"]

      db.commit()
      db.refresh(oil)

      return cls.build_response(
        data=oil.to_dict(),
        message="Aceite actualizado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al actualizar aceite: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def delete(cls, oil_id):
    db = SessionLocal()

    try:
      oil = (
        db.query(Oil)
        .filter(Oil.id == oil_id)
        .first()
      )

      if not oil:
        return cls.handle_not_found(
          "Aceite no encontrado"
        )

      db.delete(oil)
      db.commit()

      return cls.build_response(
        message="Aceite eliminado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al eliminar aceite: {str(e)}"
      )

    finally:
      db.close()