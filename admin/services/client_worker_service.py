# admin/services/client_worker_service.py

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_

from admin.models.client import Client
from admin.models.client_worker import ClientWorker
from main.databases import SessionLocal
from main.services import ApplicationService


class ClientWorkerService(ApplicationService):

  @classmethod
  def fetch_all_by_client(cls, client_id, page=1, per_page=10, search_query=None):
    db = SessionLocal()

    try:
      # Validar que el cliente exista
      client = db.query(Client).filter(Client.id == client_id).first()
      if not client:
        return cls.handle_not_found("Cliente no encontrado")

      query = db.query(ClientWorker).filter(ClientWorker.client_id == client_id)

      # SEARCH (por nombres, apellidos, correo, documento o puesto)
      if search_query:
        search_filter = f"%{search_query}%"
        query = query.filter(
          or_(
            ClientWorker.names.ilike(search_filter),
            ClientWorker.last_names.ilike(search_filter),
            ClientWorker.email.ilike(search_filter),
            ClientWorker.document.ilike(search_filter),
            ClientWorker.position.ilike(search_filter)
          )
        )

      total_workers = query.count()

      workers = (
        query
        .order_by(ClientWorker.id.asc())
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
          "client": client.to_dict(),
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
        message="Lista de trabajadores del cliente obtenida exitosamente"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al obtener trabajadores del cliente: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def fetch_one(cls, client_id, worker_id):
    db = SessionLocal()

    try:
      worker = (
        db.query(ClientWorker)
        .filter(
          ClientWorker.id == worker_id,
          ClientWorker.client_id == client_id
        )
        .first()
      )

      if not worker:
        return cls.handle_not_found(
          "Trabajador del cliente no encontrado"
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
  def create(cls, client_id, params):
    db = SessionLocal()

    try:
      # Validar que el cliente exista
      client = db.query(Client).filter(Client.id == client_id).first()
      if not client:
        return cls.handle_not_found("Cliente no encontrado")

      worker = ClientWorker(
        client_id=client_id,
        names=params.get("names"),
        last_names=params.get("last_names"),
        email=params.get("email"),
        user_id=params.get("user_id") if params.get("user_id") else None,
        document=params.get("document") if params.get("document") else None,
        phone=params.get("phone") if params.get("phone") else None,
        certification=params.get("certification") if params.get("certification") else None,
        position=params.get("position") if params.get("position") else None
      )

      db.add(worker)
      db.commit()
      db.refresh(worker)

      return cls.build_response(
        data=worker.to_dict(),
        message="Trabajador registrado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al registrar trabajador: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def update(cls, client_id, worker_id, params):
    db = SessionLocal()

    try:
      worker = (
        db.query(ClientWorker)
        .filter(
          ClientWorker.id == worker_id,
          ClientWorker.client_id == client_id
        )
        .first()
      )

      if not worker:
        return cls.handle_not_found(
          "Trabajador del cliente no encontrado"
        )

      if "names" in params:
        worker.names = params["names"]

      if "last_names" in params:
        worker.last_names = params["last_names"]

      if "email" in params:
        worker.email = params["email"]

      if "user_id" in params:
        worker.user_id = params["user_id"] if params["user_id"] else None

      if "document" in params:
        worker.document = params["document"] if params["document"] else None

      if "phone" in params:
        worker.phone = params["phone"] if params["phone"] else None

      if "certification" in params:
        worker.certification = params["certification"] if params["certification"] else None

      if "position" in params:
        worker.position = params["position"] if params["position"] else None

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
  def delete(cls, client_id, worker_id):
    db = SessionLocal()

    try:
      worker = (
        db.query(ClientWorker)
        .filter(
          ClientWorker.id == worker_id,
          ClientWorker.client_id == client_id
        )
        .first()
      )

      if not worker:
        return cls.handle_not_found(
          "Trabajador del cliente no encontrado"
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