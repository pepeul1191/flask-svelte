# admin/views/oil_type_view.py

from flask import Blueprint, flash, render_template, request, redirect

from admin.configs.middlewares import only_logged
from admin.services.oil_type_service import OilTypeService

views = Blueprint(
  "admin-oil-types-views",
  __name__,
  template_folder="../templates"
)


# =====================
# INDEX (LIST + SEARCH + PAGINATION)
# =====================
@views.route("/admin/oil-types", methods=["GET"])
@only_logged
def index():

  page = request.args.get("page", default=1, type=int)
  per_page = request.args.get("per_page", default=10, type=int)
  search_query = request.args.get("name", default='')

  if page < 1:
    page = 1

  if per_page < 1:
    per_page = 10

  response = OilTypeService.fetch_all(
    page=page,
    per_page=per_page,
    search_query=search_query
  )

  oil_types = []
  pagination = {
    "page": page,
    "per_page": per_page,
    "total_oil_types": 0,
    "total_pages": 0,
    "start_record": 0,
    "end_record": 0
  }

  if response["success"]:
    oil_types = response["data"]["oil_types"]
    pagination = response["data"]["pagination"]
  else:
    flash(response["message"], "danger")

  return render_template(
    "oil_types/index.html",
    locals={
      "title": "Tipos de Aceite",
      "nav_link": "master-data",
      "oil_types": oil_types,
      "pagination": pagination,
      "search_query": search_query
    }
  )


# =====================
# NEW
# =====================
@views.route("/admin/oil-types/new", methods=["GET"])
@only_logged
def new():

  return render_template(
    "oil_types/new.html",
    locals={
      "title": "Nuevo Tipo de Aceite",
      "nav_link": "oil-management"
    }
  )


# =====================
# CREATE
# =====================
@views.route("/admin/oil-types", methods=["POST"])
@only_logged
def create():

  response = OilTypeService.create({
    "name": request.form.get("name"),
    "description": request.form.get("description")
  })

  if response["success"]:
    flash(response["message"], "success")
    return redirect("/admin/oil-types")

  flash(response["message"], "danger")
  return redirect("/admin/oil-types/new")


# =====================
# EDIT
# =====================
@views.route("/admin/oil-types/<int:oil_type_id>/edit", methods=["GET"])
@only_logged
def edit(oil_type_id):

  response = OilTypeService.fetch_one(oil_type_id)

  if not response["success"]:
    flash(response["message"], "danger")
    return redirect("/admin/oil-types")

  return render_template(
    "oil_types/edit.html",
    locals={
      "title": "Editar Tipo de Aceite",
      "nav_link": "master-data",
      "oil_type": response["data"]
    }
  )


# =====================
# UPDATE
# =====================
@views.route("/admin/oil-types/<int:oil_type_id>/update", methods=["POST"])
@only_logged
def update(oil_type_id):

  response = OilTypeService.update(
    oil_type_id,
    {
      "name": request.form.get("name"),
      "description": request.form.get("description")
    }
  )

  if response["success"]:
    flash(response["message"], "success")
  else:
    flash(response["message"], "danger")

  return redirect(
    f"/admin/oil-types/{oil_type_id}/edit"
  )


# =====================
# DELETE
# =====================
@views.route("/admin/oil-types/<int:oil_type_id>/delete", methods=["GET"])
@only_logged
def delete(oil_type_id):

  response = OilTypeService.delete(oil_type_id)

  if response["success"]:
    flash(response["message"], "success")
  else:
    flash(response["message"], "danger")

  return redirect("/admin/oil-types")