# admin/views/branch_view.py

from flask import Blueprint, flash, render_template, request, redirect
from admin.configs.middlewares import only_logged
from admin.services.branch_service import BranchService

views = Blueprint(
  "admin-branches-views",
  __name__,
  template_folder="../templates"
)


# =========================
# LISTAR
# =========================
@views.route("/admin/branches", methods=["GET"])
@only_logged
def index():
  response = BranchService.fetch_all()

  branches = []

  if response["success"]:
    branches = response["data"]
  else:
    flash(response["message"], "danger")

  locals = {
    "title": "Sucursales",
    "nav_link": "master-data",
    "branches": branches
  }

  return render_template("branches/index.html", locals=locals)


# =========================
# NUEVO (FORM)
# =========================
@views.route("/admin/branches/new", methods=["GET"])
@only_logged
def new():
  locals = {
    "title": "Nueva Sucursal",
    "nav_link": "master-data"
  }

  return render_template("branches/new.html", locals=locals)


# =========================
# CREAR
# =========================
@views.route("/admin/branches", methods=["POST"])
@only_logged
def create():
  response = BranchService.create({
    "name": request.form.get("name"),
    "description": request.form.get("description"),
    "is_active": request.form.get("is_active") == "on"
  })

  if response["success"]:
    flash(response["message"], "success")
    return redirect("/admin/branches")

  flash(response["message"], "danger")
  return redirect("/admin/branches/new")


# =========================
# EDITAR (FORM)
# =========================
@views.route("/admin/branches/<int:branch_id>/edit", methods=["GET"])
@only_logged
def edit(branch_id):
  response = BranchService.fetch_one(branch_id)

  if not response["success"]:
    flash(response["message"], "danger")
    return redirect("/admin/branches")

  locals = {
    "title": "Editar Sucursal",
    "nav_link": "master-data",
    "branch": response["data"]
  }

  return render_template("branches/edit.html", locals=locals)


# =========================
# ACTUALIZAR
# =========================
@views.route("/admin/branches/<int:branch_id>/update", methods=["POST"])
@only_logged
def update(branch_id):
  response = BranchService.update(
    branch_id,
    {
      "name": request.form.get("name"),
      "description": request.form.get("description"),
      "is_active": request.form.get("is_active") == "on"
    }
  )

  if response["success"]:
    flash(response["message"], "success")
  else:
    flash(response["message"], "danger")

  return redirect(f"/admin/branches/{branch_id}/edit")


# =========================
# ELIMINAR
# =========================
@views.route("/admin/branches/<int:branch_id>/delete", methods=["GET"])
@only_logged
def delete(branch_id):
  response = BranchService.delete(branch_id)

  if response["success"]:
    flash(response["message"], "success")
  else:
    flash(response["message"], "danger")

  return redirect("/admin/branches")