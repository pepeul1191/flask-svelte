# admin/views/oil_view.py

from flask import Blueprint, flash, render_template, request, redirect

from admin.configs.middlewares import only_logged
from admin.services.oil_service import OilService
from admin.services.oil_brand_service import OilBrandService
from admin.services.oil_type_service import OilTypeService

views = Blueprint(
  "admin-oils-views",
  __name__,
  template_folder="../templates"
)


# =====================
# INDEX (LIST + SEARCH + FILTERS + PAGINATION)
# =====================
@views.route("/admin/oils", methods=["GET"])
@only_logged
def index():

  page = request.args.get("page", default=1, type=int)
  per_page = request.args.get("per_page", default=10, type=int)
  search_query = request.args.get("name", default='')
  
  # Filtros opcionales por marca y tipo
  oil_brand_id = request.args.get("oil_brand_id", default='', type=int) if request.args.get("oil_brand_id") else None
  oil_type_id = request.args.get("oil_type_id", default='', type=int) if request.args.get("oil_type_id") else None

  if page < 1:
    page = 1

  if per_page < 1:
    per_page = 10

  # Obtener aceites filtrados y paginados
  response = OilService.fetch_all(
    page=page,
    per_page=per_page,
    search_query=search_query,
    oil_brand_id=oil_brand_id,
    oil_type_id=oil_type_id
  )

  # Cargar marcas y tipos para poblar los selectores de búsqueda (usando per_page alto para traer todos)
  brands_response = OilBrandService.fetch_all(per_page=1000)
  types_response = OilTypeService.fetch_all(per_page=1000)

  oil_brands = brands_response["data"]["oil_brands"] if brands_response["success"] else []
  oil_types = types_response["data"]["oil_types"] if types_response["success"] else []

  oils = []
  pagination = {
    "page": page,
    "per_page": per_page,
    "total_oils": 0,
    "total_pages": 0,
    "start_record": 0,
    "end_record": 0
  }

  if response["success"]:
    oils = response["data"]["oils"]
    pagination = response["data"]["pagination"]
  else:
    flash(response["message"], "danger")

  return render_template(
    "oils/index.html",
    locals={
      "title": "Aceites",
      "nav_link": "master-data",
      "oils": oils,
      "oil_brands": oil_brands,
      "oil_types": oil_types,
      "pagination": pagination,
      "search_query": search_query,
      "selected_brand_id": oil_brand_id,
      "selected_type_id": oil_type_id
    }
  )


# =====================
# NEW
# =====================
@views.route("/admin/oils/new", methods=["GET"])
@only_logged
def new():

  # Cargar marcas y tipos para los selects del formulario de creación
  brands_response = OilBrandService.fetch_all(per_page=1000)
  types_response = OilTypeService.fetch_all(per_page=1000)

  oil_brands = brands_response["data"]["oil_brands"] if brands_response["success"] else []
  oil_types = types_response["data"]["oil_types"] if types_response["success"] else []

  return render_template(
    "oils/new.html",
    locals={
      "title": "Nuevo Aceite",
      "nav_link": "oil-management",
      "oil_brands": oil_brands,
      "oil_types": oil_types
    }
  )


# =====================
# CREATE
# =====================
@views.route("/admin/oils", methods=["POST"])
@only_logged
def create():

  response = OilService.create({
    "oil_brand_id": request.form.get("oil_brand_id"),
    "oil_type_id": request.form.get("oil_type_id"),
    "name": request.form.get("name"),
    "description": request.form.get("description")
  })

  if response["success"]:
    flash(response["message"], "success")
    return redirect("/admin/oils")

  flash(response["message"], "danger")
  return redirect("/admin/oils/new")


# =====================
# EDIT
# =====================
@views.route("/admin/oils/<int:oil_id>/edit", methods=["GET"])
@only_logged
def edit(oil_id):

  response = OilService.fetch_one(oil_id)

  if not response["success"]:
    flash(response["message"], "danger")
    return redirect("/admin/oils")

  # Cargar marcas y tipos para los selects del formulario de edición
  brands_response = OilBrandService.fetch_all(per_page=1000)
  types_response = OilTypeService.fetch_all(per_page=1000)

  oil_brands = brands_response["data"]["oil_brands"] if brands_response["success"] else []
  oil_types = types_response["data"]["oil_types"] if types_response["success"] else []

  return render_template(
    "oils/edit.html",
    locals={
      "title": "Editar Aceite",
      "nav_link": "master-data",
      "oil": response["data"],
      "oil_brands": oil_brands,
      "oil_types": oil_types
    }
  )


# =====================
# UPDATE
# =====================
@views.route("/admin/oils/<int:oil_id>/update", methods=["POST"])
@only_logged
def update(oil_id):

  response = OilService.update(
    oil_id,
    {
      "oil_brand_id": request.form.get("oil_brand_id"),
      "oil_type_id": request.form.get("oil_type_id"),
      "name": request.form.get("name"),
      "description": request.form.get("description")
    }
  )

  if response["success"]:
    flash(response["message"], "success")
  else:
    flash(response["message"], "danger")

  return redirect(
    f"/admin/oils/{oil_id}/edit"
  )


# =====================
# DELETE
# =====================
@views.route("/admin/oils/<int:oil_id>/delete", methods=["GET"])
@only_logged
def delete(oil_id):

  response = OilService.delete(oil_id)

  if response["success"]:
    flash(response["message"], "success")
  else:
    flash(response["message"], "danger")

  return redirect("/admin/oils")