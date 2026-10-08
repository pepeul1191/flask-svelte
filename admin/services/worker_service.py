# admin/services/worker_service.py

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_

from admin.models.worker import Worker
from main.databases import SessionLocal
from main.services import ApplicationService


class WorkerService(ApplicationService):

  @classmethod
  def fetch_all(cls, page=1, per_page=10, search_query=None):
    db = SessionLocal()

    try:
      query = db.query(Worker)

      # SEARCH (por nombres, apellidos, correo o documento)
      if search_query:
        search_filter = f"%{search_query}%"
        query = query.filter(
          or_(
            Worker.names.ilike(search_filter),
            Worker.last_names.ilike(search_filter),
            Worker.email.ilike(search_filter),
            Worker.document.ilike(search_filter)
          )
        )

      total_workers = query.count()

      workers = (
        query
        .order_by(Worker.id.asc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
      )

      total_pages = (
        (total_workers + per_page - 1) // per_page
      )

      start_record = (
        (page - 1) * per_page + 1
        if total_workers > 0
        else 0
      )

      end_record = min(
        page * per_page,
        total_workers
      )

      return cls.build_response(
        data={
          "workers": [
            worker.to_dict()
            for worker in workers
          ],
          "pagination": {
            "page": page,
            "per_page": per_page,
            "total_workers": total_workers,
            "total_pages": total_pages,
            "start_record": start_record,
            "end_record": end_record
          }
        },
        message="Lista de trabajadores obtenida exitosamente"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al obtener trabajadores: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def fetch_one(cls, worker_id):
    db = SessionLocal()

    try:
      worker = (
        db.query(Worker)
        .filter(Worker.id == worker_id)
        .first()
      )

      if not worker:
        return cls.handle_not_found(
          "Trabajador no encontrado"
        )

      return cls.build_response(
        data=worker.to_dict(),
        message="Trabajador encontrado"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al buscar trabajador: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def create(cls, params):
    db = SessionLocal()

    try:
      # Validar si el email ya existe
      existing_email = db.query(Worker).filter(Worker.email == params.get("email")).first()
      if existing_email:
        return cls.handle_error("El correo electrónico ya está registrado.")

      worker = Worker(
        user_id=params.get("user_id") if params.get("user_id") else None,
        names=params.get("names"),
        last_names=params.get("last_names"),
        email=params.get("email"),
        document=params.get("document"),
        phone=params.get("phone"),
        certification=params.get("certification"),
        position=params.get("position")
      )

      db.add(worker)
      db.commit()
      db.refresh(worker)

      return cls.build_response(
        data=worker.to_dict(),
        message="Trabajador creado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al crear trabajador: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def update(cls, worker_id, params):
    db = SessionLocal()

    try:
      worker = (
        db.query(Worker)
        .filter(Worker.id == worker_id)
        .first()
      )

      if not worker:
        return cls.handle_not_found(
          "Trabajador no encontrado"
        )

      # Validar unicidad de email si se está cambiando
      new_email = params.get("email")
      if new_email and new_email != worker.email:
        email_exists = db.query(Worker).filter(Worker.email == new_email).first()
        if email_exists:
          return cls.handle_error("El correo electrónico ya está en uso por otro trabajador.")
        worker.email = new_email

      if "names" in params:
        worker.names = params["names"]

      if "last_names" in params:
        worker.last_names = params["last_names"]

      if "document" in params:
        worker.document = params["document"]

      if "phone" in params:
        worker.phone = params["phone"]

      if "certification" in params:
        worker.certification = params["certification"]

      if "position" in params:
        worker.position = params["position"]

      if "user_id" in params:
        worker.user_id = params["user_id"] if params["user_id"] else None

      db.commit()
      db.refresh(worker)

      return cls.build_response(
        data=worker.to_dict(),
        message="Trabajador actualizado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al actualizar trabajador: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def delete(cls, worker_id):
    db = SessionLocal()

    try:
      worker = (
        db.query(Worker)
        .filter(Worker.id == worker_id)
        .first()
      )

      if not worker:
        return cls.handle_not_found(
          "Trabajador no encontrado"
        )

      db.delete(worker)
      db.commit()

      return cls.build_response(
        message="Trabajador eliminado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al eliminar trabajador: {str(e)}"
      )

    finally:
      db.close()