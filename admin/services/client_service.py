# admin/services/client_service.py

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_

from admin.models.client import Client
from main.databases import SessionLocal
from main.services import ApplicationService


class ClientService(ApplicationService):

  @classmethod
  def fetch_all(cls, page=1, per_page=10, search_query=None):
    db = SessionLocal()

    try:
      query = db.query(Client)

      # SEARCH (por nombre, contacto, correo o teléfono)
      if search_query:
        search_filter = f"%{search_query}%"
        query = query.filter(
          or_(
            Client.name.ilike(search_filter),
            Client.contact_name.ilike(search_filter),
            Client.email.ilike(search_filter),
            Client.phone.ilike(search_filter)
          )
        )

      total_clients = query.count()

      clients = (
        query
        .order_by(Client.id.asc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
      )

      total_pages = (
        (total_clients + per_page - 1) // per_page
      )

      start_record = (
        (page - 1) * per_page + 1
        if total_clients > 0
        else 0
      )

      end_record = min(
        page * per_page,
        total_clients
      )

      return cls.build_response(
        data={
          "clients": [
            client.to_dict()
            for client in clients
          ],
          "pagination": {
            "page": page,
            "per_page": per_page,
            "total_clients": total_clients,
            "total_pages": total_pages,
            "start_record": start_record,
            "end_record": end_record
          }
        },
        message="Lista de clientes obtenida exitosamente"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al obtener clientes: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def fetch_one(cls, client_id):
    db = SessionLocal()

    try:
      client = (
        db.query(Client)
        .filter(Client.id == client_id)
        .first()
      )

      if not client:
        return cls.handle_not_found(
          "Cliente no encontrado"
        )

      return cls.build_response(
        data=client.to_dict(),
        message="Cliente encontrado"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al buscar cliente: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def create(cls, params):
    db = SessionLocal()

    try:
      client = Client(
        name=params.get("name"),
        contact_name=params.get("contact_name"),
        email=params.get("email") if params.get("email") else None,
        phone=params.get("phone") if params.get("phone") else None,
        address=params.get("address") if params.get("address") else None,
        notes=params.get("notes") if params.get("notes") else None
      )

      db.add(client)
      db.commit()
      db.refresh(client)

      return cls.build_response(
        data=client.to_dict(),
        message="Cliente creado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al crear cliente: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def update(cls, client_id, params):
    db = SessionLocal()

    try:
      client = (
        db.query(Client)
        .filter(Client.id == client_id)
        .first()
      )

      if not client:
        return cls.handle_not_found(
          "Cliente no encontrado"
        )

      if "name" in params:
        client.name = params["name"]

      if "contact_name" in params:
        client.contact_name = params["contact_name"]

      if "email" in params:
        client.email = params["email"] if params["email"] else None

      if "phone" in params:
        client.phone = params["phone"] if params["phone"] else None

      if "address" in params:
        client.address = params["address"] if params["address"] else None

      if "notes" in params:
        client.notes = params["notes"] if params["notes"] else None

      db.commit()
      db.refresh(client)

      return cls.build_response(
        data=client.to_dict(),
        message="Cliente actualizado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al actualizar cliente: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def delete(cls, client_id):
    db = SessionLocal()

    try:
      client = (
        db.query(Client)
        .filter(Client.id == client_id)
        .first()
      )

      if not client:
        return cls.handle_not_found(
          "Cliente no encontrado"
        )

      db.delete(client)
      db.commit()

      return cls.build_response(
        message="Cliente eliminado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al eliminar cliente: {str(e)}"
      )

    finally:
      db.close()