# admin/services/phone_service.py

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import desc

from admin.models.phone import Phone
from admin.models.person import Person
from main.databases import SessionLocal
from main.services import ApplicationService


class PhoneService(ApplicationService):

  @classmethod
  def create(cls, params):
    """Crea un nuevo teléfono"""
    db = SessionLocal()

    try:
      # Validar que la persona existe
      person_id = params.get("person_id")
      if not person_id:
        return cls.handle_error("El campo person_id es requerido")

      person = db.query(Person).filter(Person.id == person_id).first()
      if not person:
        return cls.handle_not_found("Persona no encontrada")

      # Validar que el teléfono no esté vacío
      phone_number = params.get("phone", "").strip()
      if not phone_number:
        return cls.handle_error("El número de teléfono es requerido")

      # Crear el teléfono
      phone = Phone(
        person_id=person_id,
        description=params.get("description", "").strip(),
        phone=phone_number
      )

      db.add(phone)
      db.commit()
      db.refresh(phone)

      return cls.build_response(
        data=phone.to_dict(),
        message="Teléfono creado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al crear teléfono: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def update(cls, phone_id, params):
    """Actualiza un teléfono existente"""
    db = SessionLocal()

    try:
      # Buscar el teléfono
      phone = (
        db.query(Phone)
        .filter(Phone.id == phone_id)
        .first()
      )

      if not phone:
        return cls.handle_not_found("Teléfono no encontrado")

      # Si se actualiza person_id, validar que la persona existe
      if "person_id" in params:
        person_id = params["person_id"]
        person = db.query(Person).filter(Person.id == person_id).first()
        if not person:
          return cls.handle_not_found("Persona no encontrada")
        phone.person_id = person_id

      # Actualizar campos
      if "description" in params:
        phone.description = params["description"].strip()

      if "phone" in params:
        phone_number = params["phone"].strip()
        if not phone_number:
          return cls.handle_error("El número de teléfono no puede estar vacío")
        phone.phone = phone_number

      db.commit()
      db.refresh(phone)

      return cls.build_response(
        data=phone.to_dict(),
        message="Teléfono actualizado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al actualizar teléfono: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def delete(cls, phone_id):
    """Elimina un teléfono"""
    db = SessionLocal()

    try:
      phone = (
        db.query(Phone)
        .filter(Phone.id == phone_id)
        .first()
      )

      if not phone:
        return cls.handle_not_found("Teléfono no encontrado")

      # Guardar información para la respuesta
      phone_data = phone.to_dict()

      db.delete(phone)
      db.commit()

      return cls.build_response(
        data=phone_data,
        message="Teléfono eliminado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al eliminar teléfono: {str(e)}"
      )

    finally:
      db.close()
