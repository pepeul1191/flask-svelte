# admin/services/oil_brand_service.py

from sqlalchemy.exc import SQLAlchemyError

from admin.models.oil_brand import OilBrand
from main.databases import SessionLocal
from main.services import ApplicationService


class OilBrandService(ApplicationService):

  @classmethod
  def fetch_all(cls, page=1, per_page=10, search_query=None):
    db = SessionLocal()

    try:
      query = db.query(OilBrand)

      # SEARCH
      if search_query:
        query = query.filter(
          OilBrand.name.ilike(f"%{search_query}%")
        )

      total_oil_brands = query.count()

      oil_brands = (
        query
        .order_by(OilBrand.id.asc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
      )

      total_pages = (
        (total_oil_brands + per_page - 1) // per_page
      )

      start_record = (
        (page - 1) * per_page + 1
        if total_oil_brands > 0
        else 0
      )

      end_record = min(
        page * per_page,
        total_oil_brands
      )

      return cls.build_response(
        data={
          "oil_brands": [
            oil_brand.to_dict()
            for oil_brand in oil_brands
          ],
          "pagination": {
            "page": page,
            "per_page": per_page,
            "total_oil_brands": total_oil_brands,
            "total_pages": total_pages,
            "start_record": start_record,
            "end_record": end_record
          }
        },
        message="Lista de marcas de aceite obtenida exitosamente"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al obtener marcas de aceite: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def fetch_one(cls, oil_brand_id):
    db = SessionLocal()

    try:
      oil_brand = (
        db.query(OilBrand)
        .filter(OilBrand.id == oil_brand_id)
        .first()
      )

      if not oil_brand:
        return cls.handle_not_found(
          "Marca de aceite no encontrada"
        )

      return cls.build_response(
        data=oil_brand.to_dict(),
        message="Marca de aceite encontrada"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al buscar marca de aceite: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def create(cls, params):
    db = SessionLocal()

    try:
      oil_brand = OilBrand(
        name=params.get("name"),
        description=params.get("description")
      )

      db.add(oil_brand)
      db.commit()
      db.refresh(oil_brand)

      return cls.build_response(
        data=oil_brand.to_dict(),
        message="Marca de aceite creada exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al crear marca de aceite: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def update(cls, oil_brand_id, params):
    db = SessionLocal()

    try:
      oil_brand = (
        db.query(OilBrand)
        .filter(OilBrand.id == oil_brand_id)
        .first()
      )

      if not oil_brand:
        return cls.handle_not_found(
          "Marca de aceite no encontrada"
        )

      if "name" in params:
        oil_brand.name = params["name"]

      if "description" in params:
        oil_brand.description = params["description"]

      db.commit()
      db.refresh(oil_brand)

      return cls.build_response(
        data=oil_brand.to_dict(),
        message="Marca de aceite actualizada exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al actualizar marca de aceite: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def delete(cls, oil_brand_id):
    db = SessionLocal()

    try:
      oil_brand = (
        db.query(OilBrand)
        .filter(OilBrand.id == oil_brand_id)
        .first()
      )

      if not oil_brand:
        return cls.handle_not_found(
          "Marca de aceite no encontrada"
        )

      db.delete(oil_brand)
      db.commit()

      return cls.build_response(
        message="Marca de aceite eliminada exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al eliminar marca de aceite: {str(e)}"
      )

    finally:
      db.close()