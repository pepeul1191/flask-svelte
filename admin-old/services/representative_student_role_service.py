# admin/services/representative_student_role_service.py

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from admin.models.representative import Representative
from admin.models.student import Student
from admin.models.person import Person
from admin.models.representative_role import RepresentativeRole
from admin.models.representative_student_role import RepresentativeStudentRole

from main.databases import SessionLocal
from main.services import ApplicationService


class RepresentativeStudentRoleService(ApplicationService):

  @classmethod
  def fetch_by_student(
    cls,
    student_id,
    related="all",
    page=1,
    per_page=10,
    names=None,
    last_names=None,
    dni=None,
    email=None
  ):

    db = SessionLocal()

    try:

      student = (
        db.query(Student)
        .filter(
          Student.id == student_id
        )
        .first()
      )

      if not student:
        return cls.handle_not_found(
          "Alumno no encontrado"
        )

      query = (
        db.query(
          Representative,
          RepresentativeStudentRole
        )
        .join(
          Person,
          Representative.person_id == Person.id
        )
        .outerjoin(
          RepresentativeStudentRole,
          (
            (Representative.id == RepresentativeStudentRole.representative_id)
            &
            (RepresentativeStudentRole.student_id == student_id)
          )
        )
        .options(
          joinedload(Representative.person),
          joinedload(
            RepresentativeStudentRole.representative_role
          )
        )
      )

      # =========================
      # FILTERS
      # =========================

      if names:
        query = query.filter(
          Person.names.ilike(f"%{names}%")
        )

      if last_names:
        query = query.filter(
          Person.last_names.ilike(f"%{last_names}%")
        )

      if dni:
        query = query.filter(
          Person.document_number.ilike(f"%{dni}%")
        )

      if email:
        query = query.filter(
          Representative.email.ilike(f"%{email}%")
        )

      # =========================
      # RELATED FILTER
      # =========================

      if related == "related":
        query = query.filter(
          RepresentativeStudentRole.id.isnot(None)
        )

      elif related == "not_related":
        query = query.filter(
          RepresentativeStudentRole.id.is_(None)
        )

      # =========================
      # PAGINATION
      # =========================

      total_representatives = query.count()

      results = (
        query
        .order_by(
          Person.last_names.asc(),
          Person.names.asc()
        )
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
      )

      total_pages = (
        total_representatives + per_page - 1
      ) // per_page

      start_record = (
        (page - 1) * per_page + 1
        if total_representatives > 0
        else 0
      )

      end_record = min(
        page * per_page,
        total_representatives
      )

      representatives = []

      for representative, relation in results:

        representative_data = representative.to_dict()

        representative_data["relation"] = (
          {
            "id": relation.id,
            "representative_role": (
              relation.representative_role.to_dict()
              if relation.representative_role
              else None
            )
          }
          if relation
          else None
        )

        representatives.append(
          representative_data
        )

      return cls.build_response(
        data={
          "representatives": representatives,
          "pagination": {
            "page": page,
            "per_page": per_page,
            "total_representatives": total_representatives,
            "total_pages": total_pages,
            "start_record": start_record,
            "end_record": end_record
          }
        },
        message="Lista de representantes obtenida exitosamente"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al obtener representantes: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def fetch_by_representative(
    cls,
    representative_id,
    related="all",
    page=1,
    per_page=10,
    code=None,
    names=None,
    last_names=None,
    dni=None,
    email=None
  ):

    db = SessionLocal()

    try:

      representative = (
        db.query(Representative)
        .filter(
          Representative.id == representative_id
        )
        .first()
      )

      if not representative:
        return cls.handle_not_found(
          "Representante no encontrado"
        )

      query = (
        db.query(
          Student,
          RepresentativeStudentRole
        )
        .join(
          Person,
          Student.person_id == Person.id
        )
        .outerjoin(
          RepresentativeStudentRole,
          (
            (Student.id == RepresentativeStudentRole.student_id)
            &
            (
              RepresentativeStudentRole.representative_id
              == representative_id
            )
          )
        )
        .options(
          joinedload(Student.person),
          joinedload(
            RepresentativeStudentRole.representative_role
          )
        )
      )

      # =========================
      # FILTERS
      # =========================

      if code:
        query = query.filter(
          Student.code.ilike(f"%{code}%")
        )

      if names:
        query = query.filter(
          Person.names.ilike(f"%{names}%")
        )

      if last_names:
        query = query.filter(
          Person.last_names.ilike(f"%{last_names}%")
        )

      if dni:
        query = query.filter(
          Person.document_number.ilike(f"%{dni}%")
        )

      if email:
        query = query.filter(
          Student.email.ilike(f"%{email}%")
        )

      # =========================
      # RELATED FILTER
      # =========================

      if related == "related":
        query = query.filter(
          RepresentativeStudentRole.id.isnot(None)
        )

      elif related == "not_related":
        query = query.filter(
          RepresentativeStudentRole.id.is_(None)
        )

      # =========================
      # PAGINATION
      # =========================

      total_students = query.count()

      results = (
        query
        .order_by(
          Person.last_names.asc(),
          Person.names.asc()
        )
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
      )

      total_pages = (
        total_students + per_page - 1
      ) // per_page

      start_record = (
        (page - 1) * per_page + 1
        if total_students > 0
        else 0
      )

      end_record = min(
        page * per_page,
        total_students
      )

      students = []

      for student, relation in results:

        student_data = student.to_dict()

        student_data["relation"] = (
          {
            "id": relation.id,
            "representative_role": (
              relation.representative_role.to_dict()
              if relation.representative_role
              else None
            )
          }
          if relation
          else None
        )

        students.append(
          student_data
        )

      return cls.build_response(
        data={
          "students": students,
          "pagination": {
            "page": page,
            "per_page": per_page,
            "total_students": total_students,
            "total_pages": total_pages,
            "start_record": start_record,
            "end_record": end_record
          }
        },
        message="Lista de alumnos obtenida exitosamente"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al obtener alumnos: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def fetch_one(cls, relation_id):
    db = SessionLocal()

    try:

      relation = (
        db.query(RepresentativeStudentRole)
        .options(
          joinedload(RepresentativeStudentRole.representative),
          joinedload(RepresentativeStudentRole.student),
          joinedload(RepresentativeStudentRole.representative_role)
        )
        .filter(
          RepresentativeStudentRole.id == relation_id
        )
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

      representative = (
        db.query(Representative)
        .filter(
          Representative.id == params.get("representative_id")
        )
        .first()
      )

      if not representative:
        return cls.handle_not_found(
          "Representante no encontrado"
        )

      student = (
        db.query(Student)
        .filter(
          Student.id == params.get("student_id")
        )
        .first()
      )

      if not student:
        return cls.handle_not_found(
          "Estudiante no encontrado"
        )

      role = (
        db.query(RepresentativeRole)
        .filter(
          RepresentativeRole.id == params.get("representative_role_id")
        )
        .first()
      )

      if not role:
        return cls.handle_not_found(
          "Rol no encontrado"
        )

      exists = (
        db.query(RepresentativeStudentRole)
        .filter(
          RepresentativeStudentRole.representative_id == params.get("representative_id"),
          RepresentativeStudentRole.student_id == params.get("student_id"),
          RepresentativeStudentRole.representative_role_id == params.get("representative_role_id")
        )
        .first()
      )

      if exists:
        return cls.handle_error(
          "La relación ya existe."
        )

      relation = RepresentativeStudentRole(
        representative_id=params.get("representative_id"),
        student_id=params.get("student_id"),
        representative_role_id=params.get("representative_role_id")
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
        db.query(RepresentativeStudentRole)
        .filter(
          RepresentativeStudentRole.id == relation_id
        )
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

  @classmethod
  def update_role(cls, relation_id, representative_role_id):

    db = SessionLocal()

    try:

      relation = (
        db.query(RepresentativeStudentRole)
        .filter(
          RepresentativeStudentRole.id == relation_id
        )
        .first()
      )

      if not relation:
        return cls.handle_not_found(
          "Relación no encontrada"
        )

      role = (
        db.query(RepresentativeRole)
        .filter(
          RepresentativeRole.id == representative_role_id
        )
        .first()
      )

      if not role:
        return cls.handle_not_found(
          "Rol no encontrado"
        )

      relation.representative_role_id = representative_role_id

      db.commit()
      db.refresh(relation)

      return cls.build_response(
        data=relation.to_dict(),
        message="Rol actualizado correctamente"
      )

    except SQLAlchemyError as e:
      db.rollback()

      return cls.handle_error(
        f"Error al actualizar rol: {str(e)}"
      )

    finally:
      db.close()