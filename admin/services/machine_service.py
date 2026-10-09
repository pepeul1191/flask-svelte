# admin/services/machine_service.py

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_

from admin.models.machine import Machine
from admin.models.client import Client
from admin.models.brand_model import BrandModel
from main.databases import SessionLocal
from main.services import ApplicationService


class MachineService(ApplicationService):

  @classmethod
  def fetch_all(cls, page=1, per_page=10, search_query=None, client_id=None):
    db = SessionLocal()

    try:
      query = db.query(Machine)

      # Filtrar por cliente si se especifica
      if client_id:
        query = query.filter(Machine.client_id == client_id)

      # SEARCH (por nombre, código o número de serie)
      if search_query:
        search_filter = f"%{search_query}%"
        query = query.filter(
          or_(
            Machine.name.ilike(search_filter),
            Machine.code.ilike(search_filter),
            Machine.serial_number.ilike(search_filter)
          )
        )

      total_machines = query.count()

      machines = (
        query
        .order_by(Machine.id.asc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
      )

      total_pages = (
        (total_machines + per_page - 1) // per_page
      )

      start_record = (
        (page - 1) * per_page + 1
        if total_machines > 0
        else 0
      )

      end_record = min(
        page * per_page,
        total_machines
      )

      # Enriquecer la data con información relacionada para la vista
      machines_data = []
      for machine in machines:
        m_dict = machine.to_dict()
        m_dict["client_name"] = machine.client.name if machine.client else "-"
        m_dict["model_name"] = machine.brand_model.name if machine.brand_model else "-"
        m_dict["brand_name"] = machine.brand_model.brand.name if machine.brand_model and machine.brand_model.brand else "-"
        machines_data.append(m_dict)

      return cls.build_response(
        data={
          "machines": machines_data,
          "pagination": {
            "page": page,
            "per_page": per_page,
            "total_machines": total_machines,
            "total_pages": total_pages,
            "start_record": start_record,
            "end_record": end_record
          }
        },
        message="Lista de máquinas obtenida exitosamente"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al obtener máquinas: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def fetch_one(cls, machine_id):
    db = SessionLocal()

    try:
      machine = db.query(Machine).filter(Machine.id == machine_id).first()

      if not machine:
        return cls.handle_not_found("Máquina no encontrada")

      m_dict = machine.to_dict()
      m_dict["client_name"] = machine.client.name if machine.client else "-"
      m_dict["model_name"] = machine.brand_model.name if machine.brand_model else "-"

      return cls.build_response(
        data=m_dict,
        message="Máquina encontrada"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al buscar máquina: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def create(cls, params):
    db = SessionLocal()

    try:
      # Validar que el cliente exista
      client_id = params.get("client_id")
      client = db.query(Client).filter(Client.id == client_id).first()
      if not client:
        return cls.handle_not_found("El cliente seleccionado no existe")

      # Validar que el modelo de marca exista
      model_id = params.get("model_id")
      brand_model = db.query(BrandModel).filter(BrandModel.id == model_id).first()
      if not brand_model:
        return cls.handle_not_found("El modelo de marca seleccionado no existe")

      machine = Machine(
        client_id=client_id,
        model_id=model_id,
        name=params.get("name"),
        code=params.get("code"),
        serial_number=params.get("serial_number") if params.get("serial_number") else None
      )

      db.add(machine)
      db.commit()
      db.refresh(machine)

      return cls.build_response(
        data=machine.to_dict(),
        message="Máquina registrada exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al registrar máquina: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def update(cls, machine_id, params):
    db = SessionLocal()

    try:
      machine = db.query(Machine).filter(Machine.id == machine_id).first()

      if not machine:
        return cls.handle_not_found("Máquina no encontrada")

      if "client_id" in params:
        client = db.query(Client).filter(Client.id == params["client_id"]).first()
        if not client:
          return cls.handle_not_found("El cliente seleccionado no existe")
        machine.client_id = params["client_id"]

      if "model_id" in params:
        brand_model = db.query(BrandModel).filter(BrandModel.id == params["model_id"]).first()
        if not brand_model:
          return cls.handle_not_found("El modelo de marca seleccionado no existe")
        machine.model_id = params["model_id"]

      if "name" in params:
        machine.name = params["name"]

      if "code" in params:
        machine.code = params["code"]

      if "serial_number" in params:
        machine.serial_number = params["serial_number"] if params["serial_number"] else None

      db.commit()
      db.refresh(machine)

      return cls.build_response(
        data=machine.to_dict(),
        message="Máquina actualizada exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al actualizar máquina: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def delete(cls, machine_id):
    db = SessionLocal()

    try:
      machine = db.query(Machine).filter(Machine.id == machine_id).first()

      if not machine:
        return cls.handle_not_found("Máquina no encontrada")

      db.delete(machine)
      db.commit()

      return cls.build_response(
        message="Máquina eliminada exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al eliminar máquina: {str(e)}"
      )

    finally:
      db.close()