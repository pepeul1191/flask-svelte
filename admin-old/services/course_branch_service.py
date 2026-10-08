# admin/services/branch_service.py

from sqlalchemy.exc import SQLAlchemyError
from admin.models.course_branch import CourseBranch
from main.databases import SessionLocal
from main.services import ApplicationService


class CourseBranchService(ApplicationService):

  @classmethod
  def fetch_all(cls):
    db = SessionLocal()

    try:
      course_branches = (
        db.query(CourseBranch)
        .order_by(CourseBranch.id.asc())
        .all()
      )

      

      return cls.build_response(
        data = [course_branch.to_dict() for course_branch in course_branches]
      )
    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al obtener los tipos de cursos listada correctamente: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def fetch_one(cls, course_branch_id):
    db = SessionLocal()

    try:
      course_branch = (
        db.query(CourseBranch)
        .filter(CourseBranch.id == course_branch_id)
        .first()
      )

      if not course_branch:
        return cls.handle_not_found(
          "Tipo de curso no encontrado"
        )

      return cls.build_response(
        data=course_branch.to_dict(),
        message="Tipo de curso encontrado"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al buscar la Tipo de curso: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def create(cls, params):
    db = SessionLocal()

    try:
      course_branch = CourseBranch(
        name=params.get("name"),
      )

      db.add(course_branch)
      db.commit()
      db.refresh(course_branch)

      return cls.build_response(
        data=course_branch.to_dict(),
        message="Tipo de curso creado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()

      return cls.handle_error(
        f"Error al crear tipo de curso: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def update(cls, course_branch_id, params):
    db = SessionLocal()

    try:
      course_branch = (
        db.query(CourseBranch)
        .filter(CourseBranch.id == course_branch_id)
        .first()
      )

      if not course_branch:
        return cls.handle_not_found(
          "Tipo de curso no encontrado"
        )

      if "name" in params:
        course_branch.name = params["name"]

      db.commit()
      db.refresh(course_branch)

      return cls.build_response(
        data=course_branch.to_dict(),
        message="Tipo de curso actualizado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()

      return cls.handle_error(
        f"Error al actualizar tipo de curso: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def delete(cls, course_branch_id):
    db = SessionLocal()

    try:
      course_branch = (
        db.query(CourseBranch)
        .filter(CourseBranch.id == course_branch_id)
        .first()
      )

      if not course_branch:
        return cls.handle_not_found(
          "Tipo de curso no encontrado"
        )

      db.delete(course_branch)
      db.commit()

      return cls.build_response(
        message="Tipo de curso eliminado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()

      return cls.handle_error(
        f"Error al eliminar tipo de curso: {str(e)}"
      )

    finally:
      db.close()