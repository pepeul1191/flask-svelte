# admin/services/representative_role_service.py

from sqlalchemy.exc import SQLAlchemyError

from admin.models.representative_role import RepresentativeRole
from main.databases import SessionLocal
from main.services import ApplicationService


class RepresentativeRoleService(ApplicationService):

  @classmethod
  def fetch_all(cls):
    db = SessionLocal()

    try:
      representative_roles = (
        db.query(RepresentativeRole)
        .order_by(RepresentativeRole.id.asc())
        .all()
      )

      return cls.build_response(
        data=[
          representative_role.to_dict()
          for representative_role in representative_roles
        ],
        message="Lista de roles de representante obtenida exitosamente"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al obtener los roles de representante: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def fetch_one(cls, representative_role_id):
    db = SessionLocal()

    try:
      representative_role = (
        db.query(RepresentativeRole)
        .filter(
          RepresentativeRole.id == representative_role_id
        )
        .first()
      )

      if not representative_role:
        return cls.handle_not_found(
          "Rol de representante no encontrado"
        )

      return cls.build_response(
        data=representative_role.to_dict(),
        message="Rol de representante encontrado"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al buscar el rol de representante: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def create(cls, params):
    db = SessionLocal()

    try:
      representative_role = RepresentativeRole(
        name=params.get("name")
      )

      db.add(representative_role)
      db.commit()
      db.refresh(representative_role)

      return cls.build_response(
        data=representative_role.to_dict(),
        message="Rol de representante creado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()

      return cls.handle_error(
        f"Error al crear rol de representante: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def update(cls, representative_role_id, params):
    db = SessionLocal()

    try:
      representative_role = (
        db.query(RepresentativeRole)
        .filter(
          RepresentativeRole.id == representative_role_id
        )
        .first()
      )

      if not representative_role:
        return cls.handle_not_found(
          "Rol de representante no encontrado"
        )

      if "name" in params:
        representative_role.name = params["name"]

      db.commit()
      db.refresh(representative_role)

      return cls.build_response(
        data=representative_role.to_dict(),
        message="Rol de representante actualizado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()

      return cls.handle_error(
        f"Error al actualizar rol de representante: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def delete(cls, representative_role_id):
    db = SessionLocal()

    try:
      representative_role = (
        db.query(RepresentativeRole)
        .filter(
          RepresentativeRole.id == representative_role_id
        )
        .first()
      )

      if not representative_role:
        return cls.handle_not_found(
          "Rol de representante no encontrado"
        )

      db.delete(representative_role)
      db.commit()

      return cls.build_response(
        message="Rol de representante eliminado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()

      return cls.handle_error(
        f"Error al eliminar rol de representante: {str(e)}"
      )

    finally:
      db.close()