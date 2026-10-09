# admin/views/machine_view.py

from flask import Blueprint, flash, render_template, request, redirect

from admin.configs.middlewares import only_logged
from admin.services.machine_service import MachineService
from admin.models.client import Client
from admin.models.brand_model import BrandModel
from main.databases import SessionLocal

views = Blueprint(
  "admin-machines-views",
  __name__,
  template_folder="../templates"
)


# =====================
# INDEX (LIST + SEARCH + PAGINATION)
# =====================
@views.route("/admin/clients/<int:client_id>/machines", methods=["GET"])
@only_logged
def index(client_id):

  page = request.args.get("page", default=1, type=int)
  per_page = request.args.get("per_page", default=10, type=int)
  search_query = request.args.get("q", default='')

  if page < 1:
    page = 1

  if per_page < 1:
    per_page = 10

  # Validar que el cliente exista y obtener su info
  db = SessionLocal()
  try:
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
      flash("Cliente no encontrado", "danger")
      return redirect("/admin/clients")
    client_dict = client.to_dict()
  finally:
    db.close()

  response = MachineService.fetch_all(
    page=page,
    per_page=per_page,
    search_query=search_query,
    client_id=client_id
  )

  if not response["success"]:
    flash(response["message"], "danger")
    return redirect(f"/admin/clients/{client_id}")

  machines = response["data"]["machines"]
  pagination = response["data"]["pagination"]

  return render_template(
    "machines/index.html",
    locals={
      "title": f"Máquinas de {client_dict['name']}",
      "nav_link": "client-management",
      "client": client_dict,
      "machines": machines,
      "pagination": pagination,
      "search_query": search_query
    }
  )


# =====================
# NEW
# =====================
@views.route("/admin/clients/<int:client_id>/machines/new", methods=["GET"])
@only_logged
def new(client_id):

  db = SessionLocal()
  try:
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
      flash("Cliente no encontrado", "danger")
      return redirect("/admin/clients")
    client_dict = client.to_dict()

    brand_models = db.query(BrandModel).order_by(BrandModel.name.asc()).all()
    models_list = []
    for bm in brand_models:
      bm_dict = bm.to_dict()
      bm_dict["brand_name"] = bm.brand.name if bm.brand else "-"
      models_list.append(bm_dict)
  finally:
    db.close()

  return render_template(
    "machines/new.html",
    locals={
      "title": f"Nueva Máquina - {client_dict['name']}",
      "nav_link": "client-management",
      "client": client_dict,
      "brand_models": models_list
    }
  )


# =====================
# CREATE
# =====================
@views.route("/admin/clients/<int:client_id>/machines", methods=["POST"])
@only_logged
def create(client_id):

  response = MachineService.create(
    {
      "client_id": client_id,
      "model_id": request.form.get("model_id"),
      "name": request.form.get("name"),
      "code": request.form.get("code"),
      "serial_number": request.form.get("serial_number")
    }
  )

  if response["success"]:
    flash(response["message"], "success")
    return redirect(f"/admin/clients/{client_id}/machines")

  flash(response["message"], "danger")
  return redirect(f"/admin/clients/{client_id}/machines/new")


# =====================
# EDIT
# =====================
@views.route("/admin/clients/<int:client_id>/machines/<int:machine_id>/edit", methods=["GET"])
@only_logged
def edit(client_id, machine_id):

  machine_response = MachineService.fetch_one(machine_id)
  if not machine_response["success"]:
    flash(machine_response["message"], "danger")
    return redirect(f"/admin/clients/{client_id}/machines")

  machine = machine_response["data"]

  # Validar que la máquina pertenezca al cliente actual
  if machine["client_id"] != client_id:
    flash("La máquina no pertenece a este cliente", "danger")
    return redirect(f"/admin/clients/{client_id}/machines")

  db = SessionLocal()
  try:
    client = db.query(Client).filter(Client.id == client_id).first()
    client_dict = client.to_dict() if client else {}

    brand_models = db.query(BrandModel).order_by(BrandModel.name.asc()).all()
    models_list = []
    for bm in brand_models:
      bm_dict = bm.to_dict()
      bm_dict["brand_name"] = bm.brand.name if bm.brand else "-"
      models_list.append(bm_dict)
  finally:
    db.close()

  return render_template(
    "machines/edit.html",
    locals={
      "title": f"Editar Máquina - {machine['name']}",
      "nav_link": "client-management",
      "client": client_dict,
      "machine": machine,
      "brand_models": models_list
    }
  )


# =====================
# UPDATE
# =====================
@views.route("/admin/clients/<int:client_id>/machines/<int:machine_id>/update", methods=["POST"])
@only_logged
def update(client_id, machine_id):

  response = MachineService.update(
    machine_id,
    {
      "client_id": client_id,
      "model_id": request.form.get("model_id"),
      "name": request.form.get("name"),
      "code": request.form.get("code"),
      "serial_number": request.form.get("serial_number")
    }
  )

  if response["success"]:
    flash(response["message"], "success")
  else:
    flash(response["message"], "danger")

  return redirect(f"/admin/clients/{client_id}/machines/{machine_id}/edit")


# =====================
# DELETE
# =====================
@views.route("/admin/clients/<int:client_id>/machines/<int:machine_id>/delete", methods=["GET"])
@only_logged
def delete(client_id, machine_id):

  response = MachineService.delete(machine_id)

  if response["success"]:
    flash(response["message"], "success")
  else:
    flash(response["message"], "danger")

  return redirect(f"/admin/clients/{client_id}/machines")