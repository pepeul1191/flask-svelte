# admin/services/brand_model_service.py

from sqlalchemy.exc import SQLAlchemyError

from admin.models.brand_model import BrandModel
from admin.models.brand import Brand
from main.databases import SessionLocal
from main.services import ApplicationService


class BrandModelService(ApplicationService):

  @classmethod
  def fetch_by_brand(cls, brand_id, page=1, per_page=10, search_query=None):
    db = SessionLocal()

    try:
      # Validar que la marca exista primero
      brand = db.query(Brand).filter(Brand.id == brand_id).first()
      if not brand:
        return cls.handle_not_found("Marca no encontrada")

      query = db.query(BrandModel).filter(BrandModel.brand_id == brand_id)

      # SEARCH
      if search_query:
        query = query.filter(
          BrandModel.name.ilike(f"%{search_query}%")
        )

      total_models = query.count()

      models = (
        query
        .order_by(BrandModel.id.asc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
      )

      total_pages = (
        (total_models + per_page - 1) // per_page
      )

      start_record = (
        (page - 1) * per_page + 1
        if total_models > 0
        else 0
      )

      end_record = min(
        page * per_page,
        total_models
      )

      return cls.build_response(
        data={
          "brand": brand.to_dict(),
          "brand_models": [
            model.to_dict()
            for model in models
          ],
          "pagination": {
            "page": page,
            "per_page": per_page,
            "total_models": total_models,
            "total_pages": total_pages,
            "start_record": start_record,
            "end_record": end_record
          }
        },
        message="Lista de modelos obtenida exitosamente"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al obtener modelos de la marca: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def fetch_one(cls, model_id):
    db = SessionLocal()

    try:
      model = (
        db.query(BrandModel)
        .filter(BrandModel.id == model_id)
        .first()
      )

      if not model:
        return cls.handle_not_found(
          "Modelo no encontrado"
        )

      return cls.build_response(
        data=model.to_dict(),
        message="Modelo encontrado"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al buscar modelo: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def create(cls, params):
    db = SessionLocal()

    try:
      brand_id = params.get("brand_id")
      
      # Validar que la marca padre exista
      brand = db.query(Brand).filter(Brand.id == brand_id).first()
      if not brand:
        return cls.handle_not_found("Marca padre no encontrada")

      model = BrandModel(
        brand_id=brand_id,
        name=params.get("name"),
        description=params.get("description")
      )

      db.add(model)
      db.commit()
      db.refresh(model)

      return cls.build_response(
        data=model.to_dict(),
        message="Modelo creado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al crear modelo: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def update(cls, model_id, params):
    db = SessionLocal()

    try:
      model = (
        db.query(BrandModel)
        .filter(BrandModel.id == model_id)
        .first()
      )

      if not model:
        return cls.handle_not_found(
          "Modelo no encontrado"
        )

      if "name" in params:
        model.name = params["name"]

      if "description" in params:
        model.description = params["description"]

      db.commit()
      db.refresh(model)

      return cls.build_response(
        data=model.to_dict(),
        message="Modelo actualizado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al actualizar modelo: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def delete(cls, model_id):
    db = SessionLocal()

    try:
      model = (
        db.query(BrandModel)
        .filter(BrandModel.id == model_id)
        .first()
      )

      if not model:
        return cls.handle_not_found(
          "Modelo no encontrado"
        )

      db.delete(model)
      db.commit()

      return cls.build_response(
        message="Modelo eliminado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al eliminar modelo: {str(e)}"
      )

    finally:
      db.close()