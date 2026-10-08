# admin/views/course_branch_view.py

from flask import Blueprint, flash, render_template, request, redirect
from admin.configs.middlewares import only_logged
from admin.services.course_branch_service import CourseBranchService

views = Blueprint(
  "admin-course_branches-views",
  __name__,
  template_folder="../templates"
)


# =========================
# LISTAR
# =========================
@views.route("/admin/course_branches", methods=["GET"])
@only_logged
def index():
  response = CourseBranchService.fetch_all()

  course_branches = []

  print(response)

  if response["success"]:
    course_branches = response["data"]
  else:
    flash(response["message"], "danger")

  locals = {
    "title": "Sucursales",
    "nav_link": "master-data",
    "course_branches": course_branches
  }

  return render_template("course_branches/index.html", locals=locals)


# =========================
# NUEVO (FORM)
# =========================
@views.route("/admin/course_branches/new", methods=["GET"])
@only_logged
def new():
  locals = {
    "title": "Nueva Sucursal",
    "nav_link": "master-data"
  }

  return render_template("course_branches/new.html", locals=locals)


# =========================
# CREAR
# =========================
@views.route("/admin/course_branches", methods=["POST"])
@only_logged
def create():
  response = CourseBranchService.create({
    "name": request.form.get("name"),
    "description": request.form.get("description"),
    "is_active": request.form.get("is_active") == "on"
  })

  if response["success"]:
    flash(response["message"], "success")
    return redirect("/admin/course_branches")

  flash(response["message"], "danger")
  return redirect("/admin/course_branches/new")


# =========================
# EDITAR (FORM)
# =========================
@views.route("/admin/course_branches/<int:branch_id>/edit", methods=["GET"])
@only_logged
def edit(branch_id):
  response = CourseBranchService.fetch_one(branch_id)

  if not response["success"]:
    flash(response["message"], "danger")
    return redirect("/admin/course_branches")

  locals = {
    "title": "Editar Sucursal",
    "nav_link": "master-data",
    "course_branch": response["data"]
  }

  return render_template("course_branches/edit.html", locals=locals)


# =========================
# ACTUALIZAR
# =========================
@views.route("/admin/course_branches/<int:branch_id>/update", methods=["POST"])
@only_logged
def update(branch_id):
  response = CourseBranchService.update(
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

  return redirect(f"/admin/course_branches/{branch_id}/edit")


# =========================
# ELIMINAR
# =========================
@views.route("/admin/course_branches/<int:branch_id>/delete", methods=["GET"])
@only_logged
def delete(branch_id):
  response = CourseBranchService.delete(branch_id)

  if response["success"]:
    flash(response["message"], "success")
  else:
    flash(response["message"], "danger")

  return redirect("/admin/course_branches")
