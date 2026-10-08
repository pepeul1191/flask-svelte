# admin/views/oil_brand_view.py

from flask import Blueprint, flash, render_template, request, redirect

from admin.configs.middlewares import only_logged
from admin.services.oil_brand_service import OilBrandService

views = Blueprint(
  "admin-oil-brands-views",
  __name__,
  template_folder="../templates"
)


# =====================
# INDEX (LIST + SEARCH + PAGINATION)
# =====================
@views.route("/admin/oil-brands", methods=["GET"])
@only_logged
def index():

  page = request.args.get("page", default=1, type=int)
  per_page = request.args.get("per_page", default=10, type=int)
  search_query = request.args.get("name", default='')

  if page < 1:
    page = 1

  if per_page < 1:
    per_page = 10

  response = OilBrandService.fetch_all(
    page=page,
    per_page=per_page,
    search_query=search_query
  )

  oil_brands = []
  pagination = {
    "page": page,
    "per_page": per_page,
    "total_oil_brands": 0,
    "total_pages": 0,
    "start_record": 0,
    "end_record": 0
  }

  if response["success"]:
    oil_brands = response["data"]["oil_brands"]
    pagination = response["data"]["pagination"]
  else:
    flash(response["message"], "danger")

  return render_template(
    "oil_brands/index.html",
    locals={
      "title": "Marcas de Aceite",
      "nav_link": "master-data",
      "oil_brands": oil_brands,
      "pagination": pagination,
      "search_query": search_query
    }
  )


# =====================
# NEW
# =====================
@views.route("/admin/oil-brands/new", methods=["GET"])
@only_logged
def new():

  return render_template(
    "oil_brands/new.html",
    locals={
      "title": "Nueva Marca de Aceite",
      "nav_link": "oil-management"
    }
  )


# =====================
# CREATE
# =====================
@views.route("/admin/oil-brands", methods=["POST"])
@only_logged
def create():

  response = OilBrandService.create({
    "name": request.form.get("name"),
    "description": request.form.get("description")
  })

  if response["success"]:
    flash(response["message"], "success")
    return redirect("/admin/oil-brands")

  flash(response["message"], "danger")
  return redirect("/admin/oil-brands/new")


# =====================
# EDIT
# =====================
@views.route("/admin/oil-brands/<int:oil_brand_id>/edit", methods=["GET"])
@only_logged
def edit(oil_brand_id):

  response = OilBrandService.fetch_one(oil_brand_id)

  if not response["success"]:
    flash(response["message"], "danger")
    return redirect("/admin/oil-brands")

  return render_template(
    "oil_brands/edit.html",
    locals={
      "title": "Editar Marca de Aceite",
      "nav_link": "master-data",
      "oil_brand": response["data"]
    }
  )


# =====================
# UPDATE
# =====================
@views.route("/admin/oil-brands/<int:oil_brand_id>/update", methods=["POST"])
@only_logged
def update(oil_brand_id):

  response = OilBrandService.update(
    oil_brand_id,
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
    f"/admin/oil-brands/{oil_brand_id}/edit"
  )


# =====================
# DELETE
# =====================
@views.route("/admin/oil-brands/<int:oil_brand_id>/delete", methods=["GET"])
@only_logged
def delete(oil_brand_id):

  response = OilBrandService.delete(oil_brand_id)

  if response["success"]:
    flash(response["message"], "success")
  else:
    flash(response["message"], "danger")

  return redirect("/admin/oil-brands")