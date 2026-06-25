# admin/services/worker_service.py

from sqlalchemy import or_, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from admin.models.worker import Worker
from admin.models.person import Person
from main.databases import SessionLocal
from main.services import ApplicationService


class WorkerService(ApplicationService):

  @classmethod
  def fetch_all(
    cls,
    page=1,
    per_page=10,
    names=None,
    last_names=None,
    dni=None,
    code=None,
    email=None
  ):

    db = SessionLocal()

    try:

      query = (
        db.query(Worker)
        .options(joinedload(Worker.person))
        .join(Person)
      )

      # =========================
      # FILTERS
      # =========================

      if names:
        query = query.filter(
          Person.names.ilike(f"%{names}%")
        )

      if last_names:
        query = query.filter(
          Person.last_names.ilike(f"%{last_names}%")
        )

      if dni:
        query = query.filter(
          Person.document_number.ilike(f"%{dni}%")
        )

      if code:
        query = query.filter(
          Worker.code.ilike(f"%{code}%")
        )

      if email:
        query = query.filter(
          Worker.email.ilike(f"%{email}%")
        )

      # =========================
      # PAGINATION
      # =========================

      total_workers = query.count()

      workers = (
        query
        .order_by(Worker.id.asc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
      )

      total_pages = (
        total_workers + per_page - 1
      ) // per_page

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
      worker = Worker(
        code=params.get("code"),
        email=params.get("email"),
        person_id=params.get("person_id")
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

      if "code" in params:
        worker.code = params["code"]

      if "email" in params:
        worker.email = params["email"]

      if "person_id" in params:
        worker.person_id = params["person_id"]

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