# admin/services/representative_service.py

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from admin.models.person import Person
from admin.models.representative import Representative
from main.databases import SessionLocal
from main.services import ApplicationService


class RepresentativeService(ApplicationService):

  @classmethod
  def fetch_all(
    cls,
    page=1,
    per_page=10,
    names=None,
    last_names=None,
    dni=None,
    email=None
  ):

    db = SessionLocal()

    try:

      query = (
        db.query(Representative)
        .options(joinedload(Representative.person))
        .join(Person)
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
      # PAGINATION
      # =========================

      total_representatives = query.count()

      representatives = (
        query
        .order_by(Representative.id.asc())
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

      return cls.build_response(
        data={
          "representatives": [
            representative.to_dict()
            for representative in representatives
          ],
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
  def fetch_one(cls, representative_id):
    db = SessionLocal()

    try:

      representative = (
        db.query(Representative)
        .options(joinedload(Representative.person))
        .filter(
          Representative.id == representative_id
        )
        .first()
      )

      if not representative:
        return cls.handle_not_found(
          "Representante no encontrado"
        )

      return cls.build_response(
        data=representative.to_dict(),
        message="Representante encontrado"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al buscar representante: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def fetch_by_person_id(cls, person_id):
    db = SessionLocal()

    try:

      representative = (
        db.query(Representative)
        .options(joinedload(Representative.person))
        .filter(
          Representative.person_id == person_id
        )
        .first()
      )

      if not representative:
        return cls.handle_not_found(
          "Representante no encontrado para esta persona"
        )

      return cls.build_response(
        data=representative.to_dict(),
        message="Representante encontrado"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al buscar representante: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def create(cls, params):
    db = SessionLocal()

    try:

      person = (
        db.query(Person)
        .filter(
          Person.id == params.get("person_id")
        )
        .first()
      )

      if not person:
        return cls.handle_not_found(
          "Persona no encontrada"
        )

      exists = (
        db.query(Representative)
        .filter(
          Representative.person_id == params.get("person_id")
        )
        .first()
      )

      if exists:
        return cls.handle_error(
          "La persona ya tiene un representante asociado."
        )

      representative = Representative(
        email=params.get("email"),
        user_id=params.get("user_id"),
        person_id=params.get("person_id")
      )

      db.add(representative)
      db.commit()
      db.refresh(representative)

      return cls.build_response(
        data=representative.to_dict(),
        message="Representante creado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()

      return cls.handle_error(
        f"Error al crear representante: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def update(
    cls,
    representative_id,
    params
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

      if "email" in params:
        representative.email = params["email"]

      if "user_id" in params:
        representative.user_id = params["user_id"]

      db.commit()
      db.refresh(representative)

      return cls.build_response(
        data=representative.to_dict(),
        message="Representante actualizado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()

      return cls.handle_error(
        f"Error al actualizar representante: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def delete(
    cls,
    representative_id
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

      db.delete(representative)
      db.commit()

      return cls.build_response(
        message="Representante eliminado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()

      return cls.handle_error(
        f"Error al eliminar representante: {str(e)}"
      )

    finally:
      db.close()