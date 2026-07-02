# admin/services/student_service.py

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_, or_, func

from admin.models.student import Student
from admin.models.person import Person
from admin.models.document_type import DocumentType
from main.databases import SessionLocal
from main.services import ApplicationService


class StudentService(ApplicationService):

  @classmethod
  def create(cls, params):
    """Crea un nuevo estudiante"""
    db = SessionLocal()

    try:
      # Validar campos requeridos
      code = params.get('code', '')
      email = params.get('email', '')
      person_id = params.get('person_id')
      user_id = params.get('user_id')

      
      if not person_id:
        return cls.handle_error("El ID de persona es requerido")

      # Validar que la persona existe
      person = db.query(Person).filter(Person.id == person_id).first()
      if not person:
        return cls.handle_not_found("Persona no encontrada")

      # Validar que el código no esté duplicado
      existing = db.query(Student).filter(Student.code == code).first()
      if existing:
        return cls.handle_error(f"Ya existe un estudiante con el código '{code}'")

      # Validar que el email no esté duplicado
      existing = db.query(Student).filter(Student.email == email).first()
      if existing:
        return cls.handle_error(f"Ya existe un estudiante con el email '{email}'")

      # Validar que la persona no tenga ya un estudiante asociado
      existing = db.query(Student).filter(Student.person_id == person_id).first()
      if existing:
        return cls.handle_error("Esta persona ya tiene un estudiante asociado")

      # Crear el estudiante
      student = Student(
        code=code,
        email=email,
        person_id=person_id,
        user_id=user_id if user_id else None
      )

      db.add(student)
      db.commit()
      db.refresh(student)

      return cls.build_response(
        data=student.to_dict(),
        message="Estudiante creado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al crear estudiante: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def update(cls, student_id, params):
    """Actualiza un estudiante existente"""
    db = SessionLocal()

    try:
      student = db.query(Student).filter(Student.id == student_id).first()
      if not student:
        return cls.handle_not_found("Estudiante no encontrado")

      # Validar campos si se proporcionan
      if 'code' in params:
        code = params['code'].strip()
        if code:
          # Validar que el código no esté duplicado (excepto para este registro)
          existing = db.query(Student).filter(
            and_(
              Student.code == code,
              Student.id != student_id
            )
          ).first()
          if existing:
            return cls.handle_error(f"Ya existe un estudiante con el código '{code}'")
          student.code = code
        else:
          return cls.handle_error("El código no puede estar vacío")

      if 'email' in params:
        email = params['email'].strip()
        if email:
          # Validar que el email no esté duplicado (excepto para este registro)
          existing = db.query(Student).filter(
            and_(
              Student.email == email,
              Student.id != student_id
            )
          ).first()
          if existing:
            return cls.handle_error(f"Ya existe un estudiante con el email '{email}'")
          student.email = email
        else:
          return cls.handle_error("El email no puede estar vacío")

      if 'user_id' in params:
        student.user_id = params['user_id'] if params['user_id'] else None

      if 'person_id' in params:
        person_id = params['person_id']
        # Validar que la persona existe
        person = db.query(Person).filter(Person.id == person_id).first()
        if not person:
          return cls.handle_not_found("Persona no encontrada")
        
        # Validar que la persona no tenga otro estudiante asociado
        existing = db.query(Student).filter(
          and_(
            Student.person_id == person_id,
            Student.id != student_id
          )
        ).first()
        if existing:
          return cls.handle_error("Esta persona ya tiene otro estudiante asociado")
        
        student.person_id = person_id

      db.commit()
      db.refresh(student)

      return cls.build_response(
        data=student.to_dict(),
        message="Estudiante actualizado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al actualizar estudiante: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def delete(cls, student_id):
    """Elimina un estudiante"""
    db = SessionLocal()

    try:
      student = db.query(Student).filter(Student.id == student_id).first()
      if not student:
        return cls.handle_not_found("Estudiante no encontrado")

      student_data = student.to_dict()

      db.delete(student)
      db.commit()

      return cls.build_response(
        data=student_data,
        message="Estudiante eliminado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al eliminar estudiante: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def fetch_one(cls, student_id):
    """Obtiene un estudiante por su ID"""
    db = SessionLocal()

    try:
      student = db.query(Student).filter(Student.id == student_id).first()
      if not student:
        return cls.handle_not_found("Estudiante no encontrado")

      return cls.build_response(
        data=student.to_dict(),
        message="Estudiante encontrado"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al obtener estudiante: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def fetch_by_person_id(cls, person_id):
    """Obtiene un estudiante por ID de persona"""
    db = SessionLocal()

    try:
      student = db.query(Student).filter(Student.person_id == person_id).first()
      if not student:
        return cls.handle_not_found("Estudiante no encontrado para esta persona")

      return cls.build_response(
        data=student.to_dict(),
        message="Estudiante encontrado"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al obtener estudiante: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def fetch_all(cls, page=1, per_page=10, names='', last_names='', dni='', code='', email=''):
    """Obtiene todos los estudiantes con paginación y filtros"""
    db = SessionLocal()

    try:
      # Construir la consulta base con joins
      query = db.query(Student).join(Person, Student.person_id == Person.id)

      # Aplicar filtros
      filters = []

      if names:
        filters.append(Person.names.ilike(f'%{names}%'))
      
      if last_names:
        filters.append(Person.last_names.ilike(f'%{last_names}%'))
      
      if dni:
        filters.append(Person.document_number.ilike(f'%{dni}%'))
      
      if code:
        filters.append(Student.code.ilike(f'%{code}%'))
      
      if email:
        filters.append(Student.email.ilike(f'%{email}%'))

      if filters:
        query = query.filter(or_(*filters))

      # Contar total de registros (sin paginación)
      total_students = query.count()

      # Calcular offset
      offset = (page - 1) * per_page

      # Aplicar paginación y ordenar
      students = query.order_by(Student.id.desc()).offset(offset).limit(per_page).all()

      # Calcular datos de paginación
      total_pages = (total_students + per_page - 1) // per_page if total_students > 0 else 0
      start_record = offset + 1 if total_students > 0 else 0
      end_record = min(offset + per_page, total_students)

      return cls.build_response(
        data={
          "students": [s.to_dict() for s in students],
          "pagination": {
            "page": page,
            "per_page": per_page,
            "total_students": total_students,
            "total_pages": total_pages,
            "start_record": start_record,
            "end_record": end_record
          }
        },
        message=f"Se encontraron {total_students} estudiantes"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al obtener estudiantes: {str(e)}"
      )

    finally:
      db.close()