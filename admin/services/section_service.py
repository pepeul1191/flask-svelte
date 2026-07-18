# admin/services/section_service.py

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_

from admin.models.section import Section
from admin.models.course import Course
from main.databases import SessionLocal
from main.services import ApplicationService


class SectionService(ApplicationService):

  @classmethod
  def fetch_by_course(cls, course_id, search_query=''):
    db = SessionLocal()

    try:
      # Verificar que el curso existe
      course = db.query(Course).filter(Course.id == course_id).first()
      if not course:
        return cls.handle_not_found("Curso no encontrado")

      query = db.query(Section).filter(Section.course_id == course_id)

      if search_query:
        query = query.filter(
          or_(
            Section.name.ilike(f"%{search_query}%"),
            Section.code.ilike(f"%{search_query}%")
          )
        )

      sections = (
        query
        .order_by(Section.name.asc())
        .all()
      )

      return cls.build_response(
        data={
          "sections": [section.to_dict() for section in sections],
          "course": course.to_dict()
        },
        message="Secciones obtenidas correctamente"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al obtener secciones: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def create(cls, course_id, params):
    db = SessionLocal()

    try:
      # Verificar que el curso existe
      course = db.query(Course).filter(Course.id == course_id).first()
      if not course:
        return cls.handle_not_found("Curso no encontrado")

      # Verificar código duplicado en el curso
      existing_section = (
        db.query(Section)
        .filter(
          Section.course_id == course_id,
          Section.code == params.get("code")
        )
        .first()
      )

      if existing_section:
        return cls.handle_error(
          "Ya existe una sección con este código en este curso",
          status_code=400
        )

      section = Section(
        name=params.get("name"),
        code=params.get("code"),
        description=params.get("description"),
        image_url=params.get("image_url"),
        course_id=course_id
      )

      db.add(section)
      db.commit()
      db.refresh(section)

      return cls.build_response(
        data=section.to_dict(),
        message="Sección creada exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al crear sección: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def fetch_one(cls, course_id, section_id):
    db = SessionLocal()

    try:
      # Verificar que el curso existe
      course = db.query(Course).filter(Course.id == course_id).first()
      if not course:
        return cls.handle_not_found("Curso no encontrado")

      section = (
        db.query(Section)
        .filter(
          Section.id == section_id,
          Section.course_id == course_id
        )
        .first()
      )

      if not section:
        return cls.handle_not_found("Sección no encontrada")

      return cls.build_response(
        data=section.to_dict(),
        message="Sección encontrada"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def update(cls, course_id, section_id, params):
    db = SessionLocal()

    try:
      # Verificar que el curso existe
      course = db.query(Course).filter(Course.id == course_id).first()
      if not course:
        return cls.handle_not_found("Curso no encontrado")

      section = (
        db.query(Section)
        .filter(
          Section.id == section_id,
          Section.course_id == course_id
        )
        .first()
      )

      if not section:
        return cls.handle_not_found("Sección no encontrada")

      # Verificar código duplicado
      if "code" in params and params["code"] != section.code:
        existing_section = (
          db.query(Section)
          .filter(
            Section.course_id == course_id,
            Section.code == params["code"],
            Section.id != section_id
          )
          .first()
        )

        if existing_section:
          return cls.handle_error(
            "Ya existe una sección con este código en este curso",
            status_code=400
          )

      if "name" in params:
        section.name = params["name"]

      if "code" in params:
        section.code = params["code"]

      if "description" in params:
        section.description = params["description"]

      if "image_url" in params:
        section.image_url = params["image_url"]

      db.commit()
      db.refresh(section)

      return cls.build_response(
        data=section.to_dict(),
        message="Sección actualizada"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def delete(cls, course_id, section_id):
    db = SessionLocal()

    try:
      # Verificar que el curso existe
      course = db.query(Course).filter(Course.id == course_id).first()
      if not course:
        return cls.handle_not_found("Curso no encontrado")

      section = (
        db.query(Section)
        .filter(
          Section.id == section_id,
          Section.course_id == course_id
        )
        .first()
      )

      if not section:
        return cls.handle_not_found("Sección no encontrada")

      db.delete(section)
      db.commit()

      return cls.build_response(
        message="Sección eliminada"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al eliminar sección: {str(e)}"
      )

    finally:
      db.close()