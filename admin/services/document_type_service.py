# admin/services/document_type_service.py

from sqlalchemy.exc import SQLAlchemyError

from admin.models.document_type import DocumentType
from main.databases import SessionLocal
from main.services import ApplicationService


class DocumentTypeService(ApplicationService):

  @classmethod
  def fetch_all(cls):
    db = SessionLocal()

    try:
      document_types = (
        db.query(DocumentType)
        .order_by(DocumentType.id.asc())
        .all()
      )

      return cls.build_response(
        data=[
          document_type.to_dict()
          for document_type in document_types
        ],
        message="Lista de tipos de documento obtenida exitosamente"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al obtener los tipos de documento: {str(e)}"
      )

    finally:
      db.close()

  @classmethod
  def fetch_one(cls, document_type_id):
    db = SessionLocal()

    try:
      document_type = (
        db.query(DocumentType)
        .filter(DocumentType.id == document_type_id)
        .first()
      )

      if not document_type:
        return cls.handle_not_found(
          "Tipo de documento no encontrado"
        )

      return cls.build_response(
        data=document_type.to_dict(),
        message="Tipo de documento encontrado"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al buscar el tipo de documento: {str(e)}"
      )

    finally:
      db.close()