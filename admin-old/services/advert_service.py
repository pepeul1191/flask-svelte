# admin/services/advert_service.py

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_

from admin.models.advert import Advert
from admin.models.section import Section
from admin.models.course import Course
from main.databases import SessionLocal
from main.services import ApplicationService


class AdvertService(ApplicationService):

  @classmethod
  def update(cls, advert_id, params):
    """
    Actualiza solamente el estado visible del anuncio
    """
    db = SessionLocal()

    try:
      advert = db.query(Advert).filter(
        Advert.id == advert_id
      ).first()

      if not advert:
        return cls.handle_not_found("Anuncio no encontrado")

      if 'visible' not in params:
        return cls.handle_error(
          "Solo se puede actualizar el estado visible"
        )

      advert.visible = params['visible']

      db.commit()
      db.refresh(advert)

      return cls.build_response(
        data=advert.to_dict(),
        message="Estado del anuncio actualizado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al actualizar anuncio: {str(e)}"
      )

    finally:
      db.close()


  @classmethod
  def delete(cls, advert_id):
    """Elimina un anuncio"""
    db = SessionLocal()

    try:
      advert = db.query(Advert).filter(
        Advert.id == advert_id
      ).first()

      if not advert:
        return cls.handle_not_found("Anuncio no encontrado")

      advert_data = advert.to_dict()

      db.delete(advert)
      db.commit()

      return cls.build_response(
        data=advert_data,
        message="Anuncio eliminado exitosamente"
      )

    except SQLAlchemyError as e:
      db.rollback()
      return cls.handle_error(
        f"Error al eliminar anuncio: {str(e)}"
      )

    finally:
      db.close()


  @classmethod
  def fetch_one(cls, advert_id):
    """Obtiene un anuncio por ID"""
    db = SessionLocal()

    try:
      advert = db.query(Advert).filter(
        Advert.id == advert_id
      ).first()

      if not advert:
        return cls.handle_not_found("Anuncio no encontrado")

      return cls.build_response(
        data=advert.to_dict(),
        message="Anuncio encontrado"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al obtener anuncio: {str(e)}"
      )

    finally:
      db.close()


  @classmethod
  def fetch_all(
    cls,
    page=1,
    per_page=10,
    published_from_start=None,
    published_from_end=None,
    course_id=None,
    section_id=None,
    visible=None
  ):
    """
    Obtiene anuncios con paginación y filtros

    Filtros:
    - published_from_start
    - published_from_end
    - course_id
    - section_id
    - visible
    """

    db = SessionLocal()

    try:
      query = (
        db.query(Advert)
        .join(
          Section,
          Advert.section_id == Section.id
        )
        .join(
          Course,
          Section.course_id == Course.id
        )
      )

      filters = []

      if published_from_start:
        filters.append(
          Advert.published_from >= published_from_start
        )

      if published_from_end:
        filters.append(
          Advert.published_from <= published_from_end
        )

      if course_id:
        filters.append(
          Course.id == course_id
        )

      if section_id:
        filters.append(
          Section.id == section_id
        )

      if visible is not None:
        filters.append(
          Advert.visible == visible
        )

      if filters:
        query = query.filter(
          and_(*filters)
        )

      total_adverts = query.count()

      offset = (page - 1) * per_page

      adverts = (
        query
        .order_by(
          Advert.created.desc()
        )
        .offset(offset)
        .limit(per_page)
        .all()
      )

      total_pages = (
        (total_adverts + per_page - 1) // per_page
        if total_adverts > 0
        else 0
      )

      start_record = (
        offset + 1
        if total_adverts > 0
        else 0
      )

      end_record = min(
        offset + per_page,
        total_adverts
      )

      return cls.build_response(
        data={
          "adverts": [
            advert.to_dict()
            for advert in adverts
          ],
          "pagination": {
            "page": page,
            "per_page": per_page,
            "total_adverts": total_adverts,
            "total_pages": total_pages,
            "start_record": start_record,
            "end_record": end_record
          }
        },
        message=f"Se encontraron {total_adverts} anuncios"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al obtener anuncios: {str(e)}"
      )

    finally:
      db.close()