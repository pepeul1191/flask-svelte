# admin/services/courses_service.py

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_
from sqlalchemy.orm import joinedload

from admin.models.course import Course
from admin.models.level import Level
from main.databases import SessionLocal
from main.services import ApplicationService


class CourseService(ApplicationService):

  @classmethod
  def fetch_by_level_with_worker(
      cls,
      level_id,
      page=1,
      per_page=30,
      search_query=''
  ):
    db = SessionLocal()

    try:
        # Verificar que el nivel existe
        level = db.query(Level).filter(Level.id == level_id).first()
        if not level:
            return cls.handle_not_found("Nivel no encontrado")

        # Query base con worker
        query = (
            db.query(Course)
            .options(joinedload(Course.worker))
            .filter(Course.level_id == level_id)
        )

        # Aplicar búsqueda
        if search_query:
            query = query.filter(
                or_(
                    Course.name.ilike(f"%{search_query}%"),
                    Course.code.ilike(f"%{search_query}%")
                )
            )

        total_courses = query.count()

        offset = (page - 1) * per_page

        courses = (
            query
            .order_by(Course.name.asc())
            .offset(offset)
            .limit(per_page)
            .all()
        )

        total_pages = (total_courses + per_page - 1) // per_page

        start_record = offset + 1 if total_courses > 0 else 0
        end_record = min(offset + per_page, total_courses)

        return cls.build_response(
            data={
                "courses": [
                    {
                        **course.to_dict(),
                        "worker": course.worker.to_dict() if course.worker else None
                    }
                    for course in courses
                ],
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total_courses": total_courses,
                    "total_pages": total_pages,
                    "start_record": start_record,
                    "end_record": end_record
                },
                "level": level.to_dict()
            },
            message="Cursos obtenidos correctamente"
        )

    except SQLAlchemyError as e:
        return cls.handle_error(
            f"Error al obtener cursos: {str(e)}"
        )

    finally:
        db.close()

  @classmethod
  def fetch_by_level(cls, level_id, page=1, per_page=30, search_query=''):
    db = SessionLocal()

    try:
      # Verificar que el nivel existe
      level = db.query(Level).filter(Level.id == level_id).first()
      if not level:
        return cls.handle_not_found("Nivel no encontrado")

      # Construir query base
      query = db.query(Course).filter(Course.level_id == level_id)

      # Aplicar búsqueda si existe
      if search_query:
        query = query.filter(
          or_(
            Course.name.ilike(f"%{search_query}%"),
            Course.code.ilike(f"%{search_query}%")
          )
        )

      # Obtener total de registros
      total_courses = query.count()

      # Calcular offset
      offset = (page - 1) * per_page

      # Obtener registros paginados
      courses = (
        query
        .order_by(Course.name.asc())
        .offset(offset)
        .limit(per_page)
        .all()
      )

      # Calcular total de páginas
      total_pages = (total_courses + per_page - 1) // per_page

      # Calcular registros mostrados
      start_record = offset + 1 if total_courses > 0 else 0
      end_record = min(offset + per_page, total_courses)

      return cls.build_response(
        data={
          "courses": [c.to_dict() for c in courses],
          "pagination": {
            "page": page,
            "per_page": per_page,
            "total_courses": total_courses,
            "total_pages": total_pages,
            "start_record": start_record,
            "end_record": end_record
          },
          "level": level.to_dict()
        },
        message="Cursos obtenidos correctamente"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al obtener cursos: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def create(cls, level_id, params):
    db = SessionLocal()

    try:
      # Verificar que el nivel existe
      level = db.query(Level).filter(Level.id == level_id).first()
      if not level:
        return cls.handle_not_found("Nivel no encontrado")

      # Verificar que el código no esté duplicado en el mismo nivel
      existing_course = (
        db.query(Course)
        .filter(
          Course.level_id == level_id,
          Course.code == params.get("code")
        )
        .first()
      )

      if existing_course:
        return cls.handle_error(
          "Ya existe un curso con este código en este nivel",
          status_code=400
        )

      course = Course(
        name=params.get("name"),
        code=params.get("code"),
        level_id=level_id,
        description=params.get("description"),
        sylabus_url=params.get("sylabus_url"),
        worker_id=params.get("worker_id")
      )

      db.add(course)
      db.commit()
      db.refresh(course)

      return cls.build_response(
        data=course.to_dict(),
        message="Curso creado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al crear curso: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def fetch_one(cls, level_id, course_id):
    db = SessionLocal()

    try:
      # Verificar que el nivel existe
      level = db.query(Level).filter(Level.id == level_id).first()
      if not level:
        return cls.handle_not_found("Nivel no encontrado")

      course = (
        db.query(Course)
        .filter(
          Course.id == course_id,
          Course.level_id == level_id
        )
        .first()
      )

      if not course:
        return cls.handle_not_found("Curso no encontrado")

      return cls.build_response(
        data=course.to_dict(),
        message="Curso encontrado"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(f"Error: {str(e)}")

    finally:
      db.close()

  @classmethod
  def update(cls, level_id, course_id, params):
    db = SessionLocal()

    try:
      # Verificar que el nivel existe
      level = db.query(Level).filter(Level.id == level_id).first()
      if not level:
        return cls.handle_not_found("Nivel no encontrado")

      course = (
        db.query(Course)
        .filter(
          Course.id == course_id,
          Course.level_id == level_id
        )
        .first()
      )

      if not course:
        return cls.handle_not_found("Curso no encontrado")

      # Verificar código duplicado si se está actualizando
      if "code" in params and params["code"] != course.code:
        existing_course = (
          db.query(Course)
          .filter(
            Course.level_id == level_id,
            Course.code == params["code"],
            Course.id != course_id
          )
          .first()
        )

        if existing_course:
          return cls.handle_error(
            "Ya existe un curso con este código en este nivel",
            status_code=400
          )

      if "name" in params:
        course.name = params["name"]

      if "code" in params:
        course.code = params["code"]

      if "description" in params:
        course.description = params["description"]

      if "sylabus_url" in params:
        course.sylabus_url = params["sylabus_url"]

      if "worker_id" in params:
        course.worker_id = params["worker_id"]

      db.commit()
      db.refresh(course)

      return cls.build_response(
        data=course.to_dict(),
        message="Curso actualizado"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(f"Error: {str(e)}")

    finally:
      db.close()

  @classmethod
  def delete(cls, level_id, course_id):
    db = SessionLocal()

    try:
      # Verificar que el nivel existe
      level = db.query(Level).filter(Level.id == level_id).first()
      if not level:
        return cls.handle_not_found("Nivel no encontrado")

      course = (
        db.query(Course)
        .filter(
          Course.id == course_id,
          Course.level_id == level_id
        )
        .first()
      )

      if not course:
        return cls.handle_not_found("Curso no encontrado")

      db.delete(course)
      db.commit()

      return cls.build_response(
        message="Curso eliminado"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al eliminar curso: {str(e)}"
      )

    finally:
      db.close()