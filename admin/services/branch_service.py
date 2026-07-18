# admin/services/branch_service.py

from sqlalchemy.exc import SQLAlchemyError
from admin.models.branch import Branch
from main.databases import SessionLocal
from main.services import ApplicationService


class BranchService(ApplicationService):

  @classmethod
  def fetch_all(cls):
    db = SessionLocal()

    try:
      branches = (
        db.query(Branch)
        .order_by(Branch.id.asc())
        .all()
      )

      return cls.build_response(
        data=[
          branch.to_dict()
          for branch in branches
        ],
        message="Lista de sucursales obtenida exitosamente"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al obtener las sucursales: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def fetch_one(cls, branch_id):
    db = SessionLocal()

    try:
      branch = (
        db.query(Branch)
        .filter(Branch.id == branch_id)
        .first()
      )

      if not branch:
        return cls.handle_not_found(
          "Sucursal no encontrada"
        )

      return cls.build_response(
        data=branch.to_dict(),
        message="Sucursal encontrada"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al buscar la sucursal: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def create(cls, params):
    db = SessionLocal()

    try:
      branch = Branch(
        name=params.get("name"),
        description=params.get("description"),
        is_active=params.get("is_active", True)
      )

      db.add(branch)
      db.commit()
      db.refresh(branch)

      return cls.build_response(
        data=branch.to_dict(),
        message="Sucursal creada exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()

      return cls.handle_error(
        f"Error al crear sucursal: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def update(cls, branch_id, params):
    db = SessionLocal()

    try:
      branch = (
        db.query(Branch)
        .filter(Branch.id == branch_id)
        .first()
      )

      if not branch:
        return cls.handle_not_found(
          "Sucursal no encontrada"
        )

      if "name" in params:
        branch.name = params["name"]

      if "description" in params:
        branch.description = params["description"]

      if "is_active" in params:
        branch.is_active = params["is_active"]

      db.commit()
      db.refresh(branch)

      return cls.build_response(
        data=branch.to_dict(),
        message="Sucursal actualizada exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()

      return cls.handle_error(
        f"Error al actualizar sucursal: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def delete(cls, branch_id):
    db = SessionLocal()

    try:
      branch = (
        db.query(Branch)
        .filter(Branch.id == branch_id)
        .first()
      )

      if not branch:
        return cls.handle_not_found(
          "Sucursal no encontrada"
        )

      db.delete(branch)
      db.commit()

      return cls.build_response(
        message="Sucursal eliminada exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()

      return cls.handle_error(
        f"Error al eliminar sucursal: {str(e)}"
      )

    finally:
      db.close()