# admin/services/brand_service.py

from sqlalchemy.exc import SQLAlchemyError

from admin.models.brand import Brand
from main.databases import SessionLocal
from main.services import ApplicationService


class BrandService(ApplicationService):

  @classmethod
  def fetch_all(cls, page=1, per_page=10, search_query=None):
    db = SessionLocal()

    try:
      query = db.query(Brand)

      # SEARCH
      if search_query:
        query = query.filter(
          Brand.name.ilike(f"%{search_query}%")
        )

      total_brands = query.count()

      brands = (
        query
        .order_by(Brand.id.asc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
      )

      total_pages = (
        (total_brands + per_page - 1) // per_page
      )

      start_record = (
        (page - 1) * per_page + 1
        if total_brands > 0
        else 0
      )

      end_record = min(
        page * per_page,
        total_brands
      )

      return cls.build_response(
        data={
          "brands": [
            brand.to_dict()
            for brand in brands
          ],
          "pagination": {
            "page": page,
            "per_page": per_page,
            "total_brands": total_brands,
            "total_pages": total_pages,
            "start_record": start_record,
            "end_record": end_record
          }
        },
        message="Lista de marcas obtenida exitosamente"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al obtener marcas: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def fetch_one(cls, brand_id):
    db = SessionLocal()

    try:
      brand = (
        db.query(Brand)
        .filter(Brand.id == brand_id)
        .first()
      )

      if not brand:
        return cls.handle_not_found(
          "Marca no encontrada"
        )

      return cls.build_response(
        data=brand.to_dict(),
        message="Marca encontrada"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al buscar marca: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def create(cls, params):
    db = SessionLocal()

    try:
      brand = Brand(
        name=params.get("name"),
        description=params.get("description")
      )

      db.add(brand)
      db.commit()
      db.refresh(brand)

      return cls.build_response(
        data=brand.to_dict(),
        message="Marca creada exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al crear marca: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def update(cls, brand_id, params):
    db = SessionLocal()

    try:
      brand = (
        db.query(Brand)
        .filter(Brand.id == brand_id)
        .first()
      )

      if not brand:
        return cls.handle_not_found(
          "Marca no encontrada"
        )

      if "name" in params:
        brand.name = params["name"]

      if "description" in params:
        brand.description = params["description"]

      db.commit()
      db.refresh(brand)

      return cls.build_response(
        data=brand.to_dict(),
        message="Marca actualizada exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al actualizar marca: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def delete(cls, brand_id):
    db = SessionLocal()

    try:
      brand = (
        db.query(Brand)
        .filter(Brand.id == brand_id)
        .first()
      )

      if not brand:
        return cls.handle_not_found(
          "Marca no encontrada"
        )

      db.delete(brand)
      db.commit()

      return cls.build_response(
        message="Marca eliminada exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al eliminar marca: {str(e)}"
      )

    finally:
      db.close()