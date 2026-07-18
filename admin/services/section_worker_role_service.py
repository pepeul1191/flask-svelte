# admin/services/section_worker_role_service.py

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from admin.models.section import Section
from admin.models.worker import Worker
from admin.models.person import Person
from admin.models.worker_role import WorkerRole
from admin.models.section_worker_role import SectionWorkerRole

from main.databases import SessionLocal
from main.services import ApplicationService


class SectionWorkerRoleService(ApplicationService):

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
        db.query(Worker, SectionWorkerRole)
        .outerjoin(
          SectionWorkerRole,
          (
            (Worker.id == SectionWorkerRole.worker_id) &
            (SectionWorkerRole.section_id == section_id)
          )
        )
        .join(Person, Worker.person_id == Person.id)
        .options(
          joinedload(Worker.person),
          joinedload(SectionWorkerRole.worker_role)
        )
      )

      # FILTERS
      if code:
        query = query.filter(Worker.code.ilike(f"%{code}%"))

      if email:
        query = query.filter(Worker.email.ilike(f"%{email}%"))

      if names:
        query = query.filter(Person.names.ilike(f"%{names}%"))

      if last_names:
        query = query.filter(Person.last_names.ilike(f"%{last_names}%"))

      # RELATED FILTER
      if related == "related":
        query = query.filter(SectionWorkerRole.id.isnot(None))

      elif related == "not_related":
        query = query.filter(SectionWorkerRole.id.is_(None))

      # PAGINATION
      total_workers = query.count()

      results = (
        query
        .order_by(Worker.code.asc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
      )

      total_pages = (total_workers + per_page - 1) // per_page

      workers = []

      for worker, relation in results:
        data = worker.to_dict()
        data["relation"] = (
          {
            "id": relation.id,
            "worker_role": (
              relation.worker_role.to_dict()
              if relation.worker_role
              else None
            )
          }
          if relation
          else None
        )
        workers.append(data)

      return cls.build_response(
        data={
          "workers": workers,
          "pagination": {
            "page": page,
            "per_page": per_page,
            "total_workers": total_workers,
            "total_pages": total_pages
          }
        },
        message="Lista de trabajadores obtenida exitosamente"
      )

    except SQLAlchemyError as e:
      return cls.handle_error(
        f"Error al obtener trabajadores: {str(e)}"
      )

    finally:
      db.close()


  @classmethod
  def fetch_by_worker(
    cls,
    worker_id,
    page=1,
    per_page=10
  ):

    db = SessionLocal()

    try:

      worker = (
        db.query(Worker)
        .filter(
          Worker.id == worker_id
        )
        .first()
      )

      if not worker:
        return cls.handle_not_found(
          "Trabajador no encontrado"
        )


      query = (
        db.query(
          Section,
          SectionWorkerRole
        )
        .join(
          SectionWorkerRole,
          Section.id == SectionWorkerRole.section_id
        )
        .filter(
          SectionWorkerRole.worker_id == worker_id
        )
        .options(
          joinedload(
            SectionWorkerRole.worker_role
          )
        )
      )


      total_sections = query.count()

      results = (
        query
        .offset(
          (page - 1) * per_page
        )
        .limit(
          per_page
        )
        .all()
      )


      sections = []

      for section, relation in results:

        data = section.to_dict()

        data["relation"] = {
          "id": relation.id,
          "worker_role": (
            relation.worker_role.to_dict()
            if relation.worker_role
            else None
          )
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
        db.query(SectionWorkerRole)
        .options(
          joinedload(
            SectionWorkerRole.section
          ),
          joinedload(
            SectionWorkerRole.worker
          ),
          joinedload(
            SectionWorkerRole.worker_role
          )
        )
        .filter(
          SectionWorkerRole.id == relation_id
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

      section = (
        db.query(Section)
        .filter(
          Section.id == params.get("section_id")
        )
        .first()
      )

      if not section:
        return cls.handle_not_found(
          "Sección no encontrada"
        )


      worker = (
        db.query(Worker)
        .filter(
          Worker.id == params.get("worker_id")
        )
        .first()
      )

      if not worker:
        return cls.handle_not_found(
          "Trabajador no encontrado"
        )


      role = (
        db.query(WorkerRole)
        .filter(
          WorkerRole.id == params.get("worker_role_id")
        )
        .first()
      )

      if not role:
        return cls.handle_not_found(
          "Rol no encontrado"
        )


      exists = (
        db.query(SectionWorkerRole)
        .filter(
          SectionWorkerRole.section_id == params.get("section_id"),
          SectionWorkerRole.worker_id == params.get("worker_id"),
          SectionWorkerRole.worker_role_id == params.get("worker_role_id")
        )
        .first()
      )


      if exists:

        return cls.handle_error(
          "La relación ya existe"
        )


      relation = SectionWorkerRole(
        section_id=params.get("section_id"),
        worker_id=params.get("worker_id"),
        worker_role_id=params.get("worker_role_id")
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
        db.query(SectionWorkerRole)
        .filter(
          SectionWorkerRole.id == relation_id
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
  def update_role(
    cls,
    relation_id,
    worker_role_id
  ):

    db = SessionLocal()

    try:

      relation = (
        db.query(SectionWorkerRole)
        .filter(
          SectionWorkerRole.id == relation_id
        )
        .first()
      )


      if not relation:

        return cls.handle_not_found(
          "Relación no encontrada"
        )


      role = (
        db.query(WorkerRole)
        .filter(
          WorkerRole.id == worker_role_id
        )
        .first()
      )


      if not role:

        return cls.handle_not_found(
          "Rol no encontrado"
        )


      relation.worker_role_id = worker_role_id

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