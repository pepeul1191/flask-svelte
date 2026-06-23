# admin/services/departments_service.py

from sqlalchemy.exc import SQLAlchemyError

from admin.models.departament import Department
from main.databases import SessionLocal
from main.services import ApplicationService


class DepartmentService(ApplicationService):

  @classmethod
  def fetch_all(cls):
    db = SessionLocal()

    try:
      departments = (
        db.query(Department)
        .order_by(Department.name.asc())
        .all()
      )

      return cls.build_response(
        data=[department.to_dict() for department in departments],
        message="Lista de departamentos obtenida exitosamente"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al obtener los departamentos: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def fetch_one(cls, department_id):
    db = SessionLocal()

    try:
      department = (
        db.query(Department)
        .filter(Department.id == department_id)
        .first()
      )

      if not department:
        return cls.handle_not_found(
          "Departamento no encontrado"
        )

      return cls.build_response(
        data=department.to_dict(),
        message="Departamento encontrado"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al buscar el departamento: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def create(cls, params):
    db = SessionLocal()

    try:
      department = Department(
        name=params.get("name")
      )

      db.add(department)
      db.commit()
      db.refresh(department)

      return cls.build_response(
        data=department.to_dict(),
        message="Departamento creado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()

      return cls.handle_error(
        f"Error al crear departamento: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def update(cls, department_id, params):
    db = SessionLocal()

    try:
      department = (
        db.query(Department)
        .filter(Department.id == department_id)
        .first()
      )

      if not department:
        return cls.handle_not_found(
          "Departamento no encontrado"
        )

      if "name" in params:
        department.name = params["name"]

      db.commit()
      db.refresh(department)

      return cls.build_response(
        data=department.to_dict(),
        message="Departamento actualizado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()

      return cls.handle_error(
        f"Error al actualizar departamento: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def delete(cls, department_id):
    db = SessionLocal()

    try:
      department = (
        db.query(Department)
        .filter(Department.id == department_id)
        .first()
      )

      if not department:
        return cls.handle_not_found(
          "Departamento no encontrado"
        )

      db.delete(department)
      db.commit()

      return cls.build_response(
        message="Departamento eliminado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()

      return cls.handle_error(
        f"Error al eliminar departamento: {str(e)}"
      )

    finally:
      db.close()