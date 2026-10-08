# admin/services/level_service.py

from sqlalchemy.exc import SQLAlchemyError

from admin.models.level import Level
from main.databases import SessionLocal
from main.services import ApplicationService


class LevelService(ApplicationService):

  @classmethod
  def fetch_all(cls, page=1, per_page=10, search_query=None):
    db = SessionLocal()

    try:
      query = db.query(Level)

      # SEARCH
      if search_query:
        query = query.filter(Level.name.ilike(f"%{search_query}%"))

      total_levels = query.count()

      levels = (
        query
        .order_by(Level.id.asc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
      )

      total_pages = (total_levels + per_page - 1) // per_page

      start_record = (page - 1) * per_page + 1 if total_levels > 0 else 0
      end_record = min(page * per_page, total_levels)

      return cls.build_response(
        data={
          "levels": [l.to_dict() for l in levels],
          "pagination": {
            "page": page,
            "per_page": per_page,
            "total_levels": total_levels,
            "total_pages": total_pages,
            "start_record": start_record,
            "end_record": end_record
          }
        },
        message="Lista de niveles obtenida exitosamente"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al obtener niveles: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def fetch_one(cls, level_id):
    db = SessionLocal()

    try:
      level = (
        db.query(Level)
        .filter(Level.id == level_id)
        .first()
      )

      if not level:
        return cls.handle_not_found("Nivel no encontrado")

      return cls.build_response(
        data=level.to_dict(),
        message="Nivel encontrado"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al buscar nivel: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def create(cls, params):
    db = SessionLocal()

    try:
      level = Level(name=params.get("name"))

      db.add(level)
      db.commit()
      db.refresh(level)

      return cls.build_response(
        data=level.to_dict(),
        message="Nivel creado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(f"Error al crear nivel: {str(e)}")

    finally:
      db.close()

  @classmethod
  def update(cls, level_id, params):
    db = SessionLocal()

    try:
      level = db.query(Level).filter(Level.id == level_id).first()

      if not level:
        return cls.handle_not_found("Nivel no encontrado")

      if "name" in params:
        level.name = params["name"]

      db.commit()
      db.refresh(level)

      return cls.build_response(
        data=level.to_dict(),
        message="Nivel actualizado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(f"Error al actualizar nivel: {str(e)}")

    finally:
      db.close()

  @classmethod
  def delete(cls, level_id):
    db = SessionLocal()

    try:
      level = db.query(Level).filter(Level.id == level_id).first()

      if not level:
        return cls.handle_not_found("Nivel no encontrado")

      db.delete(level)
      db.commit()

      return cls.build_response(
        message="Nivel eliminado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(f"Error al eliminar nivel: {str(e)}")

    finally:
      db.close()