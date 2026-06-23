# admin/views/master_data.py

from flask import Blueprint, flash, render_template, request, redirect

from admin.configs.middlewares import only_logged
from admin.services.departments_services import DepartmentService

views = Blueprint(
  "admin-locations-views",
  __name__,
  template_folder="../templates"
)


@views.route("/admin/locations", methods=["GET"])
@only_logged
def indexs():

  departments_response = DepartmentService.fetch_all()

  departments = []

  if departments_response["success"]:
    departments = departments_response["data"]
  else:
    flash(
      departments_response["message"],
      "danger"
    )

  locals = {
    "title": "Locaciones",
    "nav_link": "master-data",
    "departments": departments
  }

  return render_template(
    "locations/index.html",
    locals=locals
  )

@views.route("/admin/departments/new", methods=["GET"])
@only_logged
def department_new():

  locals = {
    "title": "Nuevo Departamento",
    "nav_link": "master-data"
  }

  return render_template(
    "locations/department_new.html",
    locals=locals
  )

@views.route("/admin/departments", methods=["POST"])
@only_logged
def department_create():

  response = DepartmentService.create({
    "name": request.form.get("name")
  })

  if response["success"]:
    flash(response["message"], "success")
    return redirect("/admin/locations")

  flash(response["message"], "alert")

  return redirect("/admin/departments/new")

@views.route("/admin/departments/<int:department_id>/delete", methods=["GET"])
@only_logged
def department_delete(department_id):

  response = DepartmentService.delete(department_id)

  if response["success"]:
    flash(response["message"], "success")
  else:
    flash(response["message"], "danger")

  return redirect("/admin/locations")

@views.route("/admin/departments/<int:department_id>/edit", methods=["GET"])
@only_logged
def department_edit(department_id):

  response = DepartmentService.fetch_one(department_id)

  if not response["success"]:
    flash(response["message"], "danger")
    return redirect("/admin/locations")

  locals = {
    "title": "Editar Departamento",
    "nav_link": "master-data",
    "department": response["data"]
  }

  return render_template(
    "locations/department_edit.html",
    locals=locals
  )

@views.route("/admin/departments/<int:department_id>/update", methods=["POST"])
@only_logged
def department_update(department_id):

  response = DepartmentService.update(
    department_id,
    {
      "name": request.form.get("name")
    }
  )

  if response["success"]:
    flash(response["message"], "success")
  else:
    flash(response["message"], "danger")

  return redirect("/admin/locations")