# admin/views/master_data.py

from flask import Blueprint, flash, render_template, request, redirect

from admin.configs.middlewares import only_logged
from admin.services.department_service import DepartmentService
from admin.services.province_service import ProvinceService
from admin.services.district_service import DistrictService

views = Blueprint(
  "admin-locations-views",
  __name__,
  template_folder="../templates"
)


@views.route("/admin/locations", methods=["GET"])
@only_logged
def indexs(
  department_id=None,
  province_id=None,
):

  if not department_id:
    department_id = request.args.get("department_id")

  if not province_id:
    province_id = request.args.get("province_id")

  # DEPARTAMENTOS
  departments = []

  departments_response = DepartmentService.fetch_all()

  if departments_response["success"]:
    departments = departments_response["data"]
  else:
    flash(
      departments_response["message"],
      "danger"
    )

  # PROVINCIAS
  provinces = []
  selected_department = None

  if department_id:

    provinces_response = (
      ProvinceService.fetch_by_department(
        department_id
      )
    )

    if provinces_response["success"]:
      provinces = provinces_response["data"]
      selected_department = int(department_id)
    else:
      flash(
        provinces_response["message"],
        "danger"
      )

  # DISTRITOS
  districts = []
  selected_province = None

  if province_id:

    districts_response = (
      DistrictService.fetch_by_province(
        province_id
      )
    )

    if districts_response["success"]:
      districts = districts_response["data"]
      selected_province = int(province_id)
    else:
      flash(
        districts_response["message"],
        "danger"
      )

  locals = {
    "title": "Locaciones",
    "nav_link": "master-data",

    "departments": departments,
    "provinces": provinces,
    "districts": districts,

    "selected_department": selected_department,
    "selected_province": selected_province
  }

  return render_template(
    "locations/index.html",
    locals=locals
  )

@views.route("/admin/departments/<int:department_id>/provinces", methods=["GET"])
@only_logged
def department_provinces(department_id):

  # Reusar la misma lógica del index
  return indexs(department_id=department_id)

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

  flash(response["message"], "danger")

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

@views.route("/admin/departments/<int:department_id>/provinces/new", methods=["GET"])
@only_logged
def province_new(department_id):
  departments_response = DepartmentService.fetch_all()

  departments = []
  if departments_response["success"]:
    departments = departments_response["data"]

  locals = {
    "title": "Nueva Provincia",
    "nav_link": "master-data",
    "departments": departments,
    "selected_department_id": department_id
  }

  return render_template(
    "locations/province_new.html",
    locals=locals
  )

# provinces

@views.route("/admin/provinces", methods=["POST"])
@only_logged
def province_create():

  response = ProvinceService.create({
    "name": request.form.get("name"),
    "department_id": request.form.get("department_id")
  })

  if response["success"]:
    flash(response["message"], "success")
    return redirect(f"/admin/locations?department_id={request.form.get("department_id")}")

  flash(response["message"], "danger")

  return redirect(f"/admin/provinces/new?department_id={request.form.get("department_id")}")

@views.route("/admin/departments/<int:department_id>/provinces/<int:province_id>/edit", methods=["GET"])
@only_logged
def province_edit(department_id, province_id):

  province_response = ProvinceService.fetch_one(province_id)

  if not province_response["success"]:
    flash(province_response["message"], "danger")
    return redirect("/admin/locations")

  departments_response = DepartmentService.fetch_all()

  departments = []
  if departments_response["success"]:
    departments = departments_response["data"]

  locals = {
    "title": "Editar Provincia",
    "nav_link": "master-data",
    "province": province_response["data"],
    "departments": departments,
    "departemnt_id": department_id,
  }

  return render_template(
    "locations/province_edit.html",
    locals=locals
  )

@views.route("/admin/departments/<int:department_id>/provinces/<int:province_id>/update", methods=["POST"])
@only_logged
def province_update(department_id, province_id):

  response = ProvinceService.update(
    province_id,
    {
      "name": request.form.get("name"),
      "department_id": department_id
    }
  )

  if response["success"]:
    flash(response["message"], "success")
  else:
    flash(response["message"], "danger")

  return redirect(f"/admin/departments/{department_id}/provinces")

@views.route("/admin/departments/<int:department_id>/provinces/<int:province_id>/delete", methods=["GET"])
@only_logged
def province_delete(department_id, province_id):

  response = ProvinceService.delete(province_id)

  if response["success"]:
    flash(response["message"], "success")
  else:
    flash(response["message"], "danger")

  return redirect(f"/admin/departments/{department_id}/provinces")

# districts

@views.route("/admin/departments/<int:department_id>/provinces/<int:province_id>/districts", methods=["GET"])
@only_logged
def department_provinces_districts(department_id, province_id):

  # Reusar la misma lógica del index
  return indexs(department_id=department_id, province_id=province_id)

@views.route(
  "/admin/departments/<int:department_id>/provinces/<int:province_id>/districts/new",
  methods=["GET"]
)
@only_logged
def district_new(department_id, province_id):

  province_response = ProvinceService.fetch_one(
    province_id
  )

  locals = {
    "title": "Nuevo Distrito",
    "nav_link": "master-data",
    "department_id": department_id,
    "province_id": province_id,
    "province_response": province_response['data']
  }

  return render_template(
    "locations/district_new.html",
    locals=locals
  )

@views.route("/admin/districts", methods=["POST"])
@only_logged
def district_create():

  department_id = request.form.get("department_id")
  province_id = request.form.get("province_id")

  response = DistrictService.create({
    "name": request.form.get("name"),
    "province_id": province_id
  })

  if response["success"]:
    flash(response["message"], "success")

    return redirect(
      f"/admin/departments/{department_id}/provinces/{province_id}/districts"
    )

  flash(response["message"], "danger")

  return redirect(
    f"/admin/departments/{department_id}/provinces/{province_id}/districts/new"
  )

@views.route(
  "/admin/departments/<int:department_id>/provinces/<int:province_id>/districts/<int:district_id>/edit",
  methods=["GET"]
)
@only_logged
def district_edit(
  department_id,
  province_id,
  district_id
):

  district_response = DistrictService.fetch_one(
    district_id
  )

  province_response = ProvinceService.fetch_one(
    province_id
  )

  if not district_response["success"]:
    flash(district_response["message"], "danger")

    return redirect(
      f"/admin/departments/{department_id}/provinces/{province_id}/districts"
    )

  print(province_response)

  locals = {
    "title": "Editar Distrito",
    "nav_link": "master-data",
    "district": district_response["data"],
    "department_id": department_id,
    "province_response": province_response['data']
  }

  return render_template(
    "locations/district_edit.html",
    locals=locals
  )

@views.route(
  "/admin/departments/<int:department_id>/provinces/<int:province_id>/districts/<int:district_id>/update",
  methods=["POST"]
)
@only_logged
def district_update(
  department_id,
  province_id,
  district_id
):

  response = DistrictService.update(
    district_id,
    {
      "name": request.form.get("name"),
      "province_id": province_id
    }
  )

  if response["success"]:
    flash(response["message"], "success")
  else:
    flash(response["message"], "danger")

  return redirect(
    f"/admin/departments/{department_id}/provinces/{province_id}/districts"
  )

@views.route(
  "/admin/departments/<int:department_id>/provinces/<int:province_id>/districts/<int:district_id>/delete",
  methods=["GET"]
)
@only_logged
def district_delete(
  department_id,
  province_id,
  district_id
):

  response = DistrictService.delete(
    district_id
  )

  if response["success"]:
    flash(response["message"], "success")
  else:
    flash(response["message"], "danger")

  return redirect(
    f"/admin/departments/{department_id}/provinces/{province_id}/districts"
  )