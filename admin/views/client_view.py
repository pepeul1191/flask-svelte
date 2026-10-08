# admin/views/client_view.py

from flask import Blueprint, flash, render_template, request, redirect

from admin.configs.middlewares import only_logged
from admin.services.client_service import ClientService

views = Blueprint(
  "admin-clients-views",
  __name__,
  template_folder="../templates"
)


# =====================
# INDEX (LIST + SEARCH + PAGINATION)
# =====================
@views.route("/admin/clients", methods=["GET"])
@only_logged
def index():

  page = request.args.get("page", default=1, type=int)
  per_page = request.args.get("per_page", default=10, type=int)
  search_query = request.args.get("q", default='')

  if page < 1:
    page = 1

  if per_page < 1:
    per_page = 10

  response = ClientService.fetch_all(
    page=page,
    per_page=per_page,
    search_query=search_query
  )

  clients = []
  pagination = {
    "page": page,
    "per_page": per_page,
    "total_clients": 0,
    "total_pages": 0,
    "start_record": 0,
    "end_record": 0
  }

  if response["success"]:
    clients = response["data"]["clients"]
    pagination = response["data"]["pagination"]
  else:
    flash(response["message"], "danger")

  return render_template(
    "clients/index.html",
    locals={
      "title": "Gestión de Clientes",
      "nav_link": "client-management",
      "clients": clients,
      "pagination": pagination,
      "search_query": search_query
    }
  )


# =====================
# NEW
# =====================
@views.route("/admin/clients/new", methods=["GET"])
@only_logged
def new():

  return render_template(
    "clients/new.html",
    locals={
      "title": "Nuevo Cliente",
      "nav_link": "client-management"
    }
  )


# =====================
# CREATE
# =====================
@views.route("/admin/clients", methods=["POST"])
@only_logged
def create():

  response = ClientService.create({
    "name": request.form.get("name"),
    "contact_name": request.form.get("contact_name"),
    "email": request.form.get("email"),
    "phone": request.form.get("phone"),
    "address": request.form.get("address"),
    "notes": request.form.get("notes")
  })

  if response["success"]:
    flash(response["message"], "success")
    return redirect("/admin/clients")

  flash(response["message"], "danger")
  return redirect("/admin/clients/new")


# =====================
# EDIT
# =====================
@views.route("/admin/clients/<int:client_id>/edit", methods=["GET"])
@only_logged
def edit(client_id):

  response = ClientService.fetch_one(client_id)

  if not response["success"]:
    flash(response["message"], "danger")
    return redirect("/admin/clients")

  return render_template(
    "clients/edit.html",
    locals={
      "title": "Editar Cliente",
      "nav_link": "client-management",
      "client": response["data"]
    }
  )


# =====================
# UPDATE
# =====================
@views.route("/admin/clients/<int:client_id>/update", methods=["POST"])
@only_logged
def update(client_id):

  response = ClientService.update(
    client_id,
    {
      "name": request.form.get("name"),
      "contact_name": request.form.get("contact_name"),
      "email": request.form.get("email"),
      "phone": request.form.get("phone"),
      "address": request.form.get("address"),
      "notes": request.form.get("notes")
    }
  )

  if response["success"]:
    flash(response["message"], "success")
  else:
    flash(response["message"], "danger")

  return redirect(
    f"/admin/clients/{client_id}/edit"
  )


# =====================
# DELETE
# =====================
@views.route("/admin/clients/<int:client_id>/delete", methods=["GET"])
@only_logged
def delete(client_id):

  response = ClientService.delete(client_id)

  if response["success"]:
    flash(response["message"], "success")
  else:
    flash(response["message"], "danger")

  return redirect("/admin/clients")