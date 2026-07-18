# admin/views/worker_role_view.py

from flask import Blueprint, flash, render_template, request, redirect
from admin.configs.middlewares import only_logged
from admin.services.worker_role_service import WorkerRoleService

views = Blueprint(
  "admin-worker-roles-views",
  __name__,
  template_folder="../templates"
)


# =========================
# LISTAR
# =========================
@views.route("/admin/worker-roles", methods=["GET"])
@only_logged
def index():
  response = WorkerRoleService.fetch_all()

  worker_roles = []

  if response["success"]:
    worker_roles = response["data"]
  else:
    flash(response["message"], "danger")

  locals = {
    "title": "Roles de Trabajador",
    "nav_link": "master-data",
    "worker_roles": worker_roles
  }

  return render_template("worker_roles/index.html", locals=locals)


# =========================
# NUEVO (FORM)
# =========================
@views.route("/admin/worker-roles/new", methods=["GET"])
@only_logged
def new():
  locals = {
    "title": "Nuevo Rol de Trabajador",
    "nav_link": "master-data"
  }

  return render_template("worker_roles/new.html", locals=locals)


# =========================
# CREAR
# =========================
@views.route("/admin/worker-roles", methods=["POST"])
@only_logged
def create():
  response = WorkerRoleService.create({
    "name": request.form.get("name")
  })

  if response["success"]:
    flash(response["message"], "success")
    return redirect("/admin/worker-roles")

  flash(response["message"], "danger")
  return redirect("/admin/worker-roles/new")


# =========================
# EDITAR (FORM)
# =========================
@views.route("/admin/worker-roles/<int:role_id>/edit", methods=["GET"])
@only_logged
def edit(role_id):
  response = WorkerRoleService.fetch_one(role_id)

  if not response["success"]:
    flash(response["message"], "danger")
    return redirect("/admin/worker-roles")

  locals = {
    "title": "Editar Rol de Trabajador",
    "nav_link": "master-data",
    "worker_role": response["data"]
  }

  return render_template("worker_roles/edit.html", locals=locals)


# =========================
# ACTUALIZAR
# =========================
@views.route("/admin/worker-roles/<int:role_id>/update", methods=["POST"])
@only_logged
def update(role_id):
  response = WorkerRoleService.update(
    role_id,
    {
      "name": request.form.get("name")
    }
  )

  if response["success"]:
    flash(response["message"], "success")
  else:
    flash(response["message"], "danger")

  return redirect(f"/admin/worker-roles/{role_id}/edit")


# =========================
# ELIMINAR
# =========================
@views.route("/admin/worker-roles/<int:role_id>/delete", methods=["GET"])
@only_logged
def delete(role_id):
  response = WorkerRoleService.delete(role_id)

  if response["success"]:
    flash(response["message"], "success")
  else:
    flash(response["message"], "danger")

  return redirect("/admin/worker-roles")