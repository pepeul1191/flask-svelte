# admin/services/section_student_service.py

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from admin.models.section import Section
from admin.models.student import Student
from admin.models.person import Person
from admin.models.section_student import SectionStudent

from main.databases import SessionLocal
from main.services import ApplicationService


class SectionStudentService(ApplicationService):

  @classmethod
  def fetch_by_section(
    cls,
    section_id,
    related="all",
    page=1,
    per_page=10,
    code=None,
    email=None,
    names=None,
    last_names=None
  ):
    db = SessionLocal()

    try:
      section = (
        db.query(Section)
        .filter(Section.id == section_id)
        .first()
      )

      if not section:
        return cls.handle_not_found(
          "Sección no encontrada"
        )

      query = (
        db.query(Student, SectionStudent)
        .outerjoin(
          SectionStudent,
          (
            (Student.id == SectionStudent.student_id) &
            (SectionStudent.section_id == section_id)
          )
        )
        .join(Person, Student.person_id == Person.id)
        .options(
          joinedload(Student.person)
        )
      )

      # FILTERS
      if code:
        query = query.filter(Student.code.ilike(f"%{code}%"))

      if email:
        query = query.filter(Student.email.ilike(f"%{email}%"))

      if names:
        query = query.filter(Person.names.ilike(f"%{names}%"))

      if last_names:
        query = query.filter(Person.last_names.ilike(f"%{last_names}%"))

      # RELATED FILTER
      if related == "related":
        query = query.filter(SectionStudent.id.isnot(None))

      elif related == "not_related":
        query = query.filter(SectionStudent.id.is_(None))

      # PAGINATION
      total_students = query.count()

      results = (
        query
        .order_by(Person.last_names.asc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
      )

      total_pages = (total_students + per_page - 1) // per_page

      students = []

      for student, relation in results:
        data = student.to_dict()
        data["relation"] = (
          {
            "id": relation.id
          }
          if relation
          else None
        )
        students.append(data)

      return cls.build_response(
        data={
          "students": students,
          "pagination": {
            "page": page,
            "per_page": per_page,
            "total_students": total_students,
            "total_pages": total_pages
          }
        },
        message="Lista de estudiantes obtenida exitosamente"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al obtener estudiantes: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def fetch_by_student(
    cls,
    student_id,
    page=1,
    per_page=10
  ):
    db = SessionLocal()

    try:
      student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
      )

      if not student:
        return cls.handle_not_found(
          "Estudiante no encontrado"
        )

      query = (
        db.query(Section, SectionStudent)
        .join(
          SectionStudent,
          Section.id == SectionStudent.section_id
        )
        .filter(
          SectionStudent.student_id == student_id
        )
        .options(
          joinedload(SectionStudent.section)
        )
      )

      total_sections = query.count()

      results = (
        query
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
      )

      sections = []

      for section, relation in results:
        data = section.to_dict()
        data["relation"] = {
          "id": relation.id
        }
        sections.append(data)

      return cls.build_response(
        data={
          "sections": sections,
          "pagination": {
            "page": page,
            "per_page": per_page,
            "total_sections": total_sections
          }
        },
        message="Lista de secciones obtenida exitosamente"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al obtener secciones: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def fetch_one(cls, relation_id):
    db = SessionLocal()

    try:
      relation = (
        db.query(SectionStudent)
        .options(
          joinedload(SectionStudent.section),
          joinedload(SectionStudent.student)
        )
        .filter(SectionStudent.id == relation_id)
        .first()
      )

      if not relation:
        return cls.handle_not_found(
          "Relación no encontrada"
        )

      return cls.build_response(
        data=relation.to_dict(),
        message="Relación encontrada"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al buscar relación: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def create(cls, params):
    db = SessionLocal()

    try:
      section = (
        db.query(Section)
        .filter(Section.id == params.get("section_id"))
        .first()
      )

      if not section:
        return cls.handle_not_found(
          "Sección no encontrada"
        )

      student = (
        db.query(Student)
        .filter(Student.id == params.get("student_id"))
        .first()
      )

      if not student:
        return cls.handle_not_found(
          "Estudiante no encontrado"
        )

      exists = (
        db.query(SectionStudent)
        .filter(
          SectionStudent.section_id == params.get("section_id"),
          SectionStudent.student_id == params.get("student_id")
        )
        .first()
      )

      if exists:
        return cls.handle_error(
          "La relación ya existe"
        )

      relation = SectionStudent(
        section_id=params.get("section_id"),
        student_id=params.get("student_id")
      )

      db.add(relation)
      db.commit()
      db.refresh(relation)

      return cls.build_response(
        data=relation.to_dict(),
        message="Relación creada exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()

      return cls.handle_error(
        f"Error al crear relación: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def delete(cls, relation_id):
    db = SessionLocal()

    try:
      relation = (
        db.query(SectionStudent)
        .filter(SectionStudent.id == relation_id)
        .first()
      )

      if not relation:
        return cls.handle_not_found(
          "Relación no encontrada"
        )

      db.delete(relation)
      db.commit()

      return cls.build_response(
        message="Relación eliminada exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()

      return cls.handle_error(
        f"Error al eliminar relación: {str(e)}"
      )

    finally:
      db.close()