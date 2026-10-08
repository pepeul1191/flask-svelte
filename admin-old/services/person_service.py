# admin/services/person_service.py

# admin/services/person_service.py

from sqlalchemy.exc import SQLAlchemyError
from admin.models.person import Person
from main.databases import SessionLocal
from main.services import ApplicationService

class PersonService(ApplicationService):

  @classmethod
  def create(cls, data):
    db = SessionLocal()
    try:
      new_person = Person(
        names=data.get('names'),
        last_names=data.get('last_names'),
        document_type_id=int(data.get('document_type_id')) if data.get('document_type_id') else None,
        document_number=data.get('document_number'),
        sex_id=int(data.get('sex_id')) if data.get('sex_id') else None,
        birth_date=data.get('birth_date') if data.get('birth_date') else None,
        image_url=data.get('image_url', 'img/user.png')
      )
      
      db.add(new_person)
      db.commit()
      db.refresh(new_person)

      return cls.build_response(
        data=new_person.to_dict(),
        message="Persona creada exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al crear la persona: {str(e)}"
      )
    finally:
      db.close()

  @classmethod
  def update(cls, person_id, data):
    db = SessionLocal()
    try:
      person = db.query(Person).filter(Person.id == person_id).first()

      if not person:
        return cls.handle_not_found("Persona no encontrada")

      person.names = data.get('names', person.names)
      person.last_names = data.get('last_names', person.last_names)
      person.document_type_id = int(data.get('document_type_id')) if data.get('document_type_id') else person.document_type_id
      person.document_number = data.get('document_number', person.document_number)
      person.sex_id = int(data.get('sex_id')) if data.get('sex_id') else person.sex_id
      person.birth_date = data.get('birth_date') if data.get('birth_date') else person.birth_date
      person.image_url = data.get('image_url', person.image_url)

      db.commit()
      db.refresh(person)

      return cls.build_response(
        data=person.to_dict(),
        message="Persona actualizada exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al actualizar la persona: {str(e)}"
      )
    finally:
      db.close()