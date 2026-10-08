from flask import Blueprint, flash, render_template, request, redirect

from admin.configs.middlewares import only_logged
from admin.services.representative_role_service import (
  RepresentativeRoleService
)

views = Blueprint(
  "admin-representative-roles-views",
  __name__,
  template_folder="../templates"
)

# =========================
# LISTAR
# =========================
@views.route("/admin/representative-roles", methods=["GET"])
@only_logged
def index():

  response = RepresentativeRoleService.fetch_all()

  representative_roles = []

  if response["success"]:
    representative_roles = response["data"]
  else:
    flash(response["message"], "danger")

  locals = {
    "title": "Roles de Representante",
    "nav_link": "master-data",
    "representative_roles": representative_roles
  }

  return render_template(
    "representative_roles/index.html",
    locals=locals
  )


# =========================
# NUEVO (FORM)
# =========================
@views.route("/admin/representative-roles/new", methods=["GET"])
@only_logged
def new():

  locals = {
    "title": "Nuevo Rol de Representante",
    "nav_link": "master-data"
  }

  return render_template(
    "representative_roles/new.html",
    locals=locals
  )


# =========================
# CREAR
# =========================
@views.route("/admin/representative-roles", methods=["POST"])
@only_logged
def create():

  response = RepresentativeRoleService.create({
    "name": request.form.get("name")
  })

  if response["success"]:
    flash(response["message"], "success")
    return redirect("/admin/representative-roles")

  flash(response["message"], "danger")
  return redirect("/admin/representative-roles/new")


# =========================
# EDITAR (FORM)
# =========================
@views.route("/admin/representative-roles/<int:role_id>/edit", methods=["GET"])
@only_logged
def edit(role_id):

  response = RepresentativeRoleService.fetch_one(role_id)

  if not response["success"]:
    flash(response["message"], "danger")
    return redirect("/admin/representative-roles")

  locals = {
    "title": "Editar Rol de Representante",
    "nav_link": "master-data",
    "representative_role": response["data"]
  }

  return render_template(
    "representative_roles/edit.html",
    locals=locals
  )


# =========================
# ACTUALIZAR
# =========================
@views.route("/admin/representative-roles/<int:role_id>/update", methods=["POST"])
@only_logged
def update(role_id):

  response = RepresentativeRoleService.update(
    role_id,
    {
      "name": request.form.get("name")
    }
  )

  if response["success"]:
    flash(response["message"], "success")
  else:
    flash(response["message"], "danger")

  return redirect(f"/admin/representative-roles/{role_id}/edit")


# =========================
# ELIMINAR
# =========================
@views.route("/admin/representative-roles/<int:role_id>/delete", methods=["GET"])
@only_logged
def delete(role_id):

  response = RepresentativeRoleService.delete(role_id)

  if response["success"]:
    flash(response["message"], "success")
  else:
    flash(response["message"], "danger")

  return redirect("/admin/representative-roles")