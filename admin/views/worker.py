# admin/views/worker.py

from flask import Blueprint, flash, render_template, request, redirect

from admin.configs.middlewares import only_logged
from admin.services.worker_service import WorkerService


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

  print(response)

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
      "nav_link": "workers",
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

  return render_template(
    "workers/new.html",
    locals={
      "title": "Nuevo Trabajador",
      "nav_link": "workers"
    }
  )


# =====================
# CREATE
# =====================
@views.route("/admin/workers", methods=["POST"])
@only_logged
def create():

  response = WorkerService.create({
    "code": request.form.get("code"),
    "email": request.form.get("email"),
    "person_id": request.form.get("person_id")
  })

  if response["success"]:
    flash(response["message"], "success")
    return redirect("/admin/workers")

  flash(response["message"], "danger")

  return redirect("/admin/workers/new")


# =====================
# EDIT
# =====================
@views.route("/admin/workers/<int:worker_id>/edit", methods=["GET"])
@only_logged
def edit(worker_id):

  response = WorkerService.fetch_one(worker_id)

  if not response["success"]:
    flash(response["message"], "danger")
    return redirect("/admin/workers")

  return render_template(
    "workers/edit.html",
    locals={
      "title": "Editar Trabajador",
      "nav_link": "workers",
      "worker": response["data"]
    }
  )


# =====================
# UPDATE
# =====================
@views.route(
  "/admin/workers/<int:worker_id>/update",
  methods=["POST"]
)
@only_logged
def update(worker_id):

  response = WorkerService.update(
    worker_id,
    {
      "code": request.form.get("code"),
      "email": request.form.get("email"),
      "person_id": request.form.get("person_id")
    }
  )

  if response["success"]:
    flash(response["message"], "success")
  else:
    flash(response["message"], "danger")

  return redirect(
    f"/admin/workers/{worker_id}/edit"
  )


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