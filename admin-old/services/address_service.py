# admin/services/address_service.py

from sqlalchemy.exc import SQLAlchemyError

from admin.models.address import Address
from admin.models.person import Person
from admin.models.vw_location import VwLocation
from main.databases import SessionLocal
from main.services import ApplicationService


class AddressService(ApplicationService):

  @classmethod
  def create(cls, params):
    """Crea una nueva dirección"""
    db = SessionLocal()

    try:
      # Validar que la persona existe
      person_id = params.get("person_id")
      if not person_id:
        return cls.handle_error("El campo person_id es requerido")

      person = db.query(Person).filter(Person.id == person_id).first()
      if not person:
        return cls.handle_not_found("Persona no encontrada")

      # Validar que el distrito existe
      district_id = params.get("district_id")
      if not district_id:
        return cls.handle_error("El campo district_id es requerido")

      district = db.query(VwLocation).filter(VwLocation.id == district_id).first()
      if not district:
        return cls.handle_not_found("Distrito no encontrado")

      # Validar que la dirección no esté vacía
      address_text = params.get("address", "").strip()
      if not address_text:
        return cls.handle_error("La dirección es requerida")

      # Crear la dirección
      address = Address(
        person_id=person_id,
        district_id=district_id,
        address=address_text,
        description=params.get("description", "").strip()
      )

      db.add(address)
      db.commit()
      db.refresh(address)

      return cls.build_response(
        data=address.to_dict(),
        message="Dirección creada exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al crear dirección: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def update(cls, address_id, params):
    """Actualiza una dirección existente"""
    db = SessionLocal()

    try:
      # Buscar la dirección
      address = (
        db.query(Address)
        .filter(Address.id == address_id)
        .first()
      )

      if not address:
        return cls.handle_not_found("Dirección no encontrada")

      # Si se actualiza person_id, validar que la persona existe
      if "person_id" in params:
        person_id = params["person_id"]
        person = db.query(Person).filter(Person.id == person_id).first()
        if not person:
          return cls.handle_not_found("Persona no encontrada")
        address.person_id = person_id

      # Si se actualiza district_id, validar que el distrito existe
      if "district_id" in params:
        district_id = params["district_id"]
        district = db.query(VwLocation).filter(VwLocation.id == district_id).first()
        if not district:
          return cls.handle_not_found("Distrito no encontrado")
        address.district_id = district_id

      # Actualizar campos
      if "description" in params:
        address.description = params["description"].strip()

      if "address" in params:
        address_text = params["address"].strip()
        if not address_text:
          return cls.handle_error("La dirección no puede estar vacía")
        address.address = address_text

      db.commit()
      db.refresh(address)

      return cls.build_response(
        data=address.to_dict(),
        message="Dirección actualizada exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al actualizar dirección: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def delete(cls, address_id):
    """Elimina una dirección"""
    db = SessionLocal()

    try:
      address = (
        db.query(Address)
        .filter(Address.id == address_id)
        .first()
      )

      if not address:
        return cls.handle_not_found("Dirección no encontrada")

      # Guardar información para la respuesta
      address_data = address.to_dict()

      db.delete(address)
      db.commit()

      return cls.build_response(
        data=address_data,
        message="Dirección eliminada exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al eliminar dirección: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def fetch_one(cls, address_id):
    """Obtiene una dirección por su ID"""
    db = SessionLocal()

    try:
      address = (
        db.query(Address)
        .filter(Address.id == address_id)
        .first()
      )

      if not address:
        return cls.handle_not_found("Dirección no encontrada")

      return cls.build_response(
        data=address.to_dict(),
        message="Dirección encontrada"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al obtener dirección: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def fetch_by_person(cls, person_id):
    """Obtiene todas las direcciones de una persona"""
    db = SessionLocal()

    try:
      addresses = (
        db.query(Address)
        .filter(Address.person_id == person_id)
        .all()
      )

      return cls.build_response(
        data=[a.to_dict() for a in addresses],
        message=f"Se encontraron {len(addresses)} direcciones"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al obtener direcciones: {str(e)}"
      )

    finally:
      db.close()