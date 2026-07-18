# admin/views/section_worker_role_view.py

from flask import Blueprint, flash, render_template, request, redirect
from admin.configs.middlewares import only_logged
from admin.services.section_worker_role_service import SectionWorkerRoleService
from admin.services.section_service import SectionService
from admin.services.worker_service import WorkerService
from admin.services.worker_role_service import WorkerRoleService

views = Blueprint(
  "admin-section-workers-views",
  __name__,
  template_folder="../templates"
)


# =========================
# LISTAR TRABAJADORES
# =========================
@views.route(
  "/admin/levels/<int:level_id>/courses/<int:course_id>/sections/<int:section_id>/workers",
  methods=["GET"]
)
@only_logged
def index(level_id, course_id, section_id):
  # Obtener filtros de la URL
  filters = {
    "names": request.args.get("names", ""),
    "last_names": request.args.get("last_names", ""),
    "code": request.args.get("code", ""),
    "email": request.args.get("email", ""),
    "related": request.args.get("related", "all"),
    "page": int(request.args.get("page", 1)),
    "per_page": int(request.args.get("per_page", 10))
  }

  response = SectionWorkerRoleService.fetch_by_section(
    section_id,
    related=filters["related"],
    page=filters["page"],
    per_page=filters["per_page"],
    code=filters["code"],
    email=filters["email"],
    names=filters["names"],
    last_names=filters["last_names"]
  )

  workers = []
  pagination = None
  worker_roles = []

  if response["success"]:
    workers = response["data"]["workers"]
    pagination = response["data"]["pagination"]
    # Obtener roles disponibles para los filtros
    roles_response = WorkerRoleService.fetch_all()
    worker_roles = roles_response["data"] if roles_response["success"] else []
  else:
    flash(response["message"], "danger")

  section_response = SectionService.fetch_one(course_id, section_id)

  locals = {
    "title": "Trabajadores de la sección",
    "nav_link": "academic-management",
    "level_id": level_id,
    "course_id": course_id,
    "section_id": section_id,
    "section": section_response["data"] if section_response["success"] else None,
    "workers": workers,
    "pagination": pagination,
    "filters": filters,  # Filtros para mantener en la vista
    "worker_roles": worker_roles  # Roles para el selector
  }

  return render_template("sections/workers.html", locals=locals)
  return render_template("sections/workers.html", locals=locals)


