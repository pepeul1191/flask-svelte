# admin/views/worker.py

from flask import Blueprint, flash, render_template, request, redirect

from admin.configs.middlewares import only_logged
from admin.services.person_service import PersonService
from admin.services.worker_service import WorkerService
from admin.services.sex_service import SexService
from admin.services.document_type_service import DocumentTypeService
from admin.services.phone_service import PhoneService
from admin.models.person import Person


views = Blueprint(
  "admin-workers-views",
  __name__,
  template_folder="../templates"
)


# =====================
# INDEX (LIST + SEARCH + PAGINATION)
# =====================
@views.route("/admin/workers", methods=["GET"])
@only_logged
def index():

  page = request.args.get("page", default=1, type=int)
  per_page = request.args.get("per_page", default=10, type=int)

  # 🔥 NUEVOS FILTROS
  names = request.args.get("names", default="")
  last_names = request.args.get("last_names", default="")
  dni = request.args.get("dni", default="")
  code = request.args.get("code", default="")
  email = request.args.get("email", default="")

  if page < 1:
    page = 1

  if per_page < 1:
    per_page = 10

  response = WorkerService.fetch_all(
    page=page,
    per_page=per_page,
    names=names,
    last_names=last_names,
    dni=dni,
    code=code,
    email=email
  )

  workers = []

  pagination = {
    "page": page,
    "per_page": per_page,
    "total_workers": 0,
    "total_pages": 0,
    "start_record": 0,
    "end_record": 0
  }

  # 🔥 IMPORTANTE: enviamos filtros al template
  filters = {
    "names": names,
    "last_names": last_names,
    "dni": dni,
    "code": code,
    "email": email
  }

  if response["success"]:
    workers = response["data"]["workers"]
    pagination = response["data"]["pagination"]
  else:
    flash(response["message"], "danger")

  return render_template(
    "workers/index.html",
    locals={
      "title": "Trabajadores",
      "nav_link": "worker-management",
      "workers": workers,
      "pagination": pagination,
      "filters": filters
    }
  )


# =====================
# NEW
# =====================
@views.route("/admin/workers/new", methods=["GET"])
@only_logged
def new():
  sexes_response = SexService.fetch_all()
  document_types_response = DocumentTypeService.fetch_all()

  sexes = []
  document_types = []

  if sexes_response["success"]:
    sexes = sexes_response["data"]
  else:
    flash(sexes_response["message"], "danger")

  if document_types_response["success"]:
    document_types = document_types_response["data"]
  else:
    flash(document_types_response["message"], "danger")

  return render_template(
    "workers/new.html",
    locals={
        "title": "Nuevo Trabajador",
        "nav_link": "worker-management",
        "sexes": sexes,
        "document_types": document_types,
      }
    )


# =====================
# CREATE WORKER FROM PERSON
# =====================
@views.route("/admin/workers/personal", methods=["POST"])
@only_logged
def create():

  # 1. Crear la persona en PersonService
  person_response = PersonService.create({
    "names": request.form.get("names"),
    "last_names": request.form.get("last_names"),
    "document_type_id": request.form.get("document_type_id"),
    "document_number": request.form.get("document_number"),
    "sex_id": request.form.get("sex_id"),
    "birth_date": request.form.get("birth_date"),
    "image_url": request.form.get("image_url")
  })

  if not person_response["success"]:
    flash(person_response["message"], "danger")
    return redirect("/admin/workers/new")

  # 2. Con el id de la persona creada, se genera el registro del trabajador
  person_id = person_response["data"]["id"]
  worker_response = WorkerService.create({
    "code": request.form.get("document_number"),
    "email": request.form.get("email"),
    "person_id": person_id
  })

  if worker_response["success"]:
    flash(worker_response["message"], "success")
    worker_id = worker_response["data"]["id"]
    return redirect(f"/admin/workers/{worker_id}/edit")

  flash(worker_response["message"], "danger")
  return redirect("/admin/workers/new")


# =====================
# EDIT
# =====================
@views.route("/admin/workers/<int:worker_id>/edit", methods=["GET"])
@only_logged
def edit(worker_id):

  response = WorkerService.fetch_one(worker_id)

  sexes_response = SexService.fetch_all()
  document_types_response = DocumentTypeService.fetch_all()

  if not response["success"]:
    flash(response["message"], "danger")
    return redirect("/admin/workers")
  
  sexes = []
  document_types = []

  if sexes_response["success"]:
    sexes = sexes_response["data"]
  else:
    flash(sexes_response["message"], "danger")

  if document_types_response["success"]:
    document_types = document_types_response["data"]
  else:
    flash(document_types_response["message"], "danger")

  return render_template(
    "workers/edit.html",
    locals={
      "title": "Editar Trabajador",
      "nav_link": "worker-management",
      "worker": response["data"],
      "person": response["data"]["person"],
      "sexes": sexes,
      "document_types": document_types,
    }
  )


# =====================
# UPDATE
# =====================
@views.route("/admin/workers/personal/<int:person_id>/edit", methods=["POST"])
@only_logged
def edit_personal(person_id):

  response = PersonService.update(person_id, {
    "names": request.form.get("names"),
    "last_names": request.form.get("last_names"),
    "document_type_id": request.form.get("document_type_id"),
    "document_number": request.form.get("document_number"),
    "sex_id": request.form.get("sex_id"),
    "birth_date": request.form.get("birth_date"),
    "image_url": request.form.get("image_url")
  })

  if response["success"]:
    # Buscamos el trabajador asociado a esa persona usando WorkerService
    worker_response = WorkerService.fetch_by_person_id(person_id)
    
    if worker_response["success"]:
      flash(response["message"], "success")
      worker_id = worker_response["data"]["id"]
      return redirect(f"/admin/workers/{worker_id}/edit")
    
    # En caso de que la persona se actualice pero no se encuentre su Worker
    flash("Persona actualizada, pero no se encontró el trabajador asociado.", "warning")
    return redirect(request.referrer)

  flash(response["message"], "danger")
  return redirect(request.referrer)

@views.route("/admin/workers/<int:worker_id>/edit", methods=["POST"])
@only_logged
def edit_worker(worker_id):

  response = WorkerService.update(worker_id, {
    "code": request.form.get("code"),
    "email": request.form.get("email"),
    "user_id": request.form.get("user_id"),
    "bio": request.form.get("bio"),
  })

  if response["success"]:
    # En caso de que la persona se actualice pero no se encuentre su Worker
    flash("Trabajador actualizado.", "success")
    return redirect(f"/admin/workers/{worker_id}/edit")

  flash(response["message"], "danger")
  return redirect(request.referrer)

# =====================
# DELETE
# =====================
@views.route(
  "/admin/workers/<int:worker_id>/delete",
  methods=["GET"]
)
@only_logged
def delete(worker_id):

  response = WorkerService.delete(worker_id)

  if response["success"]:
    flash(response["message"], "success")
  else:
    flash(response["message"], "danger")

  return redirect("/admin/workers")
