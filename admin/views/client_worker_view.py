# admin/views/client_worker_view.py

from flask import Blueprint, flash, render_template, request, redirect

from admin.configs.middlewares import only_logged
from admin.services.client_worker_service import ClientWorkerService

views = Blueprint(
  "admin-client-workers-views",
  __name__,
  template_folder="../templates"
)


# =====================
# INDEX (LIST + SEARCH + PAGINATION)
# =====================
@views.route("/admin/clients/<int:client_id>/workers", methods=["GET"])
@only_logged
def index(client_id):

  page = request.args.get("page", default=1, type=int)
  per_page = request.args.get("per_page", default=10, type=int)
  search_query = request.args.get("q", default='')

  if page < 1:
    page = 1

  if per_page < 1:
    per_page = 10

  response = ClientWorkerService.fetch_all_by_client(
    client_id=client_id,
    page=page,
    per_page=per_page,
    search_query=search_query
  )

  if not response["success"]:
    flash(response["message"], "danger")
    return redirect("/admin/clients")

  client = response["data"]["client"]
  workers = response["data"]["workers"]
  pagination = response["data"]["pagination"]

  return render_template(
    "client_workers/index.html",
    locals={
      "title": f"Trabajadores de {client['name']}",
      "nav_link": "client-management",
      "client": client,
      "workers": workers,
      "pagination": pagination,
      "search_query": search_query
    }
  )


# =====================
# NEW
# =====================
@views.route("/admin/clients/<int:client_id>/workers/new", methods=["GET"])
@only_logged
def new(client_id):

  # Validar que el cliente exista obteniendo la data básica
  response = ClientWorkerService.fetch_all_by_client(client_id=client_id, page=1, per_page=1)
  if not response["success"]:
    flash(response["message"], "danger")
    return redirect("/admin/clients")

  client = response["data"]["client"]

  return render_template(
    "client_workers/new.html",
    locals={
      "title": f"Nuevo Trabajador - {client['name']}",
      "nav_link": "client-management",
      "client": client
    }
  )


# =====================
# CREATE
# =====================
@views.route("/admin/clients/<int:client_id>/workers", methods=["POST"])
@only_logged
def create(client_id):

  response = ClientWorkerService.create(
    client_id,
    {
      "names": request.form.get("names"),
      "last_names": request.form.get("last_names"),
      "email": request.form.get("email"),
      "user_id": request.form.get("user_id"),
      "document": request.form.get("document"),
      "phone": request.form.get("phone"),
      "certification": request.form.get("certification"),
      "position": request.form.get("position")
    }
  )

  if response["success"]:
    flash(response["message"], "success")
    return redirect(f"/admin/clients/{client_id}/workers")

  flash(response["message"], "danger")
  return redirect(f"/admin/clients/{client_id}/workers/new")


# =====================
# EDIT
# =====================
@views.route("/admin/clients/<int:client_id>/workers/<int:worker_id>/edit", methods=["GET"])
@only_logged
def edit(client_id, worker_id):

  # Obtener el cliente y el trabajador
  client_response = ClientWorkerService.fetch_all_by_client(client_id=client_id, page=1, per_page=1)
  if not client_response["success"]:
    flash(client_response["message"], "danger")
    return redirect("/admin/clients")

  client = client_response["data"]["client"]

  worker_response = ClientWorkerService.fetch_one(client_id, worker_id)
  if not worker_response["success"]:
    flash(worker_response["message"], "danger")
    return redirect(f"/admin/clients/{client_id}/workers")

  return render_template(
    "client_workers/edit.html",
    locals={
      "title": f"Editar Trabajador - {client['name']}",
      "nav_link": "client-management",
      "client": client,
      "worker": worker_response["data"]
    }
  )


# =====================
# UPDATE
# =====================
@views.route("/admin/clients/<int:client_id>/workers/<int:worker_id>/update", methods=["POST"])
@only_logged
def update(client_id, worker_id):

  response = ClientWorkerService.update(
    client_id,
    worker_id,
    {
      "names": request.form.get("names"),
      "last_names": request.form.get("last_names"),
      "email": request.form.get("email"),
      "user_id": request.form.get("user_id"),
      "document": request.form.get("document"),
      "phone": request.form.get("phone"),
      "certification": request.form.get("certification"),
      "position": request.form.get("position")
    }
  )

  if response["success"]:
    flash(response["message"], "success")
  else:
    flash(response["message"], "danger")

  return redirect(
    f"/admin/clients/{client_id}/workers/{worker_id}/edit"
  )


# =====================
# DELETE
# =====================
@views.route("/admin/clients/<int:client_id>/workers/<int:worker_id>/delete", methods=["GET"])
@only_logged
def delete(client_id, worker_id):

  response = ClientWorkerService.delete(client_id, worker_id)

  if response["success"]:
    flash(response["message"], "success")
  else:
    flash(response["message"], "danger")

  return redirect(f"/admin/clients/{client_id}/workers")