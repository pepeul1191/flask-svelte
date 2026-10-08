# admin/views/brand_view.py

from flask import Blueprint, flash, render_template, request, redirect

from admin.configs.middlewares import only_logged
from admin.services.brand_service import BrandService

views = Blueprint(
  "admin-brands-views",
  __name__,
  template_folder="../templates"
)


# =====================
# INDEX (LIST + SEARCH + PAGINATION)
# =====================
@views.route("/admin/brands", methods=["GET"])
@only_logged
def index():

  page = request.args.get("page", default=1, type=int)
  per_page = request.args.get("per_page", default=10, type=int)
  search_query = request.args.get("name", default='')

  if page < 1:
    page = 1

  if per_page < 1:
    per_page = 10

  response = BrandService.fetch_all(
    page=page,
    per_page=per_page,
    search_query=search_query
  )

  brands = []
  pagination = {
    "page": page,
    "per_page": per_page,
    "total_brands": 0,
    "total_pages": 0,
    "start_record": 0,
    "end_record": 0
  }

  if response["success"]:
    brands = response["data"]["brands"]
    pagination = response["data"]["pagination"]
  else:
    flash(response["message"], "danger")

  return render_template(
    "brands/index.html",
    locals={
      "title": "Marcas de Equipos",
      "nav_link": "master-data",
      "brands": brands,
      "pagination": pagination,
      "search_query": search_query
    }
  )


# =====================
# NEW
# =====================
@views.route("/admin/brands/new", methods=["GET"])
@only_logged
def new():

  return render_template(
    "brands/new.html",
    locals={
      "title": "Nueva Marca",
      "nav_link": "master-data"
    }
  )


# =====================
# CREATE
# =====================
@views.route("/admin/brands", methods=["POST"])
@only_logged
def create():

  response = BrandService.create({
    "name": request.form.get("name"),
    "description": request.form.get("description")
  })

  if response["success"]:
    flash(response["message"], "success")
    return redirect("/admin/brands")

  flash(response["message"], "danger")
  return redirect("/admin/brands/new")


# =====================
# EDIT
# =====================
@views.route("/admin/brands/<int:brand_id>/edit", methods=["GET"])
@only_logged
def edit(brand_id):

  response = BrandService.fetch_one(brand_id)

  if not response["success"]:
    flash(response["message"], "danger")
    return redirect("/admin/brands")

  return render_template(
    "brands/edit.html",
    locals={
      "title": "Editar Marca",
      "nav_link": "master-data",
      "brand": response["data"]
    }
  )


# =====================
# UPDATE
# =====================
@views.route("/admin/brands/<int:brand_id>/update", methods=["POST"])
@only_logged
def update(brand_id):

  response = BrandService.update(
    brand_id,
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
    f"/admin/brands/{brand_id}/edit"
  )


# =====================
# DELETE
# =====================
@views.route("/admin/brands/<int:brand_id>/delete", methods=["GET"])
@only_logged
def delete(brand_id):

  response = BrandService.delete(brand_id)

  if response["success"]:
    flash(response["message"], "success")
  else:
    flash(response["message"], "danger")

  return redirect("/admin/brands")