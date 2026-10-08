# admin/views/worker_view.py

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
  search_query = request.args.get("q", default='')

  if page < 1:
    page = 1

  if per_page < 1:
    per_page = 10

  response = WorkerService.fetch_all(
    page=page,
    per_page=per_page,
    search_query=search_query
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

  if response["success"]:
    workers = response["data"]["workers"]
    pagination = response["data"]["pagination"]
  else:
    flash(response["message"], "danger")

  return render_template(
    "workers/index.html",
    locals={
      "title": "Gestión de Trabajadores",
      "nav_link": "worker-management",
      "workers": workers,
      "pagination": pagination,
      "search_query": search_query
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
      "nav_link": "worker-management"
    }
  )


# =====================
# CREATE
# =====================
@views.route("/admin/workers", methods=["POST"])
@only_logged
def create():

  response = WorkerService.create({
    "names": request.form.get("names"),
    "last_names": request.form.get("last_names"),
    "email": request.form.get("email"),
    "document": request.form.get("document"),
    "phone": request.form.get("phone"),
    "certification": request.form.get("certification"),
    "position": request.form.get("position"),
    "user_id": request.form.get("user_id")
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

  print('1 ++++++++++++++++++++++++++++++++++')
  print(response["data"])
  print('2 ++++++++++++++++++++++++++++++++++')

  return render_template(
    "workers/edit.html",
    locals={
      "title": "Editar Trabajador",
      "nav_link": "worker-management",
      "worker": response["data"]
    }
  )


# =====================
# UPDATE
# =====================
@views.route("/admin/workers/<int:worker_id>/update", methods=["POST"])
@only_logged
def update(worker_id):

  response = WorkerService.update(
    worker_id,
    {
      "names": request.form.get("names"),
      "last_names": request.form.get("last_names"),
      "email": request.form.get("email"),
      "document": request.form.get("document"),
      "phone": request.form.get("phone"),
      "certification": request.form.get("certification"),
      "position": request.form.get("position"),
      "user_id": request.form.get("user_id")
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
@views.route("/admin/workers/<int:worker_id>/delete", methods=["GET"])
@only_logged
def delete(worker_id):

  response = WorkerService.delete(worker_id)

  if response["success"]:
    flash(response["message"], "success")
  else:
    flash(response["message"], "danger")

  return redirect("/admin/workers")