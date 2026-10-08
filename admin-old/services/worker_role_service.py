# admin/services/worker_role_service.py

from sqlalchemy.exc import SQLAlchemyError
from admin.models.worker_role import WorkerRole
from main.databases import SessionLocal
from main.services import ApplicationService


class WorkerRoleService(ApplicationService):

  @classmethod
  def fetch_all(cls):
    db = SessionLocal()

    try:
      worker_roles = (
        db.query(WorkerRole)
        .order_by(WorkerRole.id.asc())
        .all()
      )

      return cls.build_response(
        data=[
          worker_role.to_dict()
          for worker_role in worker_roles
        ],
        message="Lista de roles de trabajadores obtenida exitosamente"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al obtener los roles de trabajadores: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def fetch_one(cls, worker_role_id):
    db = SessionLocal()

    try:
      worker_role = (
        db.query(WorkerRole)
        .filter(WorkerRole.id == worker_role_id)
        .first()
      )

      if not worker_role:
        return cls.handle_not_found(
          "Rol de trabajador no encontrado"
        )

      return cls.build_response(
        data=worker_role.to_dict(),
        message="Rol de trabajador encontrado"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al buscar el rol de trabajador: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def create(cls, params):
    db = SessionLocal()

    try:
      worker_role = WorkerRole(
        name=params.get("name")
      )

      db.add(worker_role)
      db.commit()
      db.refresh(worker_role)

      return cls.build_response(
        data=worker_role.to_dict(),
        message="Rol de trabajador creado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()

      return cls.handle_error(
        f"Error al crear rol de trabajador: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def update(cls, worker_role_id, params):
    db = SessionLocal()

    try:
      worker_role = (
        db.query(WorkerRole)
        .filter(WorkerRole.id == worker_role_id)
        .first()
      )

      if not worker_role:
        return cls.handle_not_found(
          "Rol de trabajador no encontrado"
        )

      if "name" in params:
        worker_role.name = params["name"]

      db.commit()
      db.refresh(worker_role)

      return cls.build_response(
        data=worker_role.to_dict(),
        message="Rol de trabajador actualizado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()

      return cls.handle_error(
        f"Error al actualizar rol de trabajador: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def delete(cls, worker_role_id):
    db = SessionLocal()

    try:
      worker_role = (
        db.query(WorkerRole)
        .filter(WorkerRole.id == worker_role_id)
        .first()
      )

      if not worker_role:
        return cls.handle_not_found(
          "Rol de trabajador no encontrado"
        )

      db.delete(worker_role)
      db.commit()

      return cls.build_response(
        message="Rol de trabajador eliminado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()

      return cls.handle_error(
        f"Error al eliminar rol de trabajador: {str(e)}"
      )

    finally:
      db.close()