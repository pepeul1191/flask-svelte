# admin/views/master_data.py

from flask import Blueprint, flash, render_template

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
      "alert"
    )

  locals = {
    "title": "Locaciones",
    "nav_link": "master-data",
    "departments": departments
  }

  return render_template(
    "locations.html",
    locals=locals
  )