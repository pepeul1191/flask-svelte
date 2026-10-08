# admin/views/brand_model_view.py

from flask import Blueprint, flash, render_template, request, redirect

from admin.configs.middlewares import only_logged
from admin.services.brand_model_service import BrandModelService

views = Blueprint(
  "admin-brand-models-views",
  __name__,
  template_folder="../templates"
)


# =====================
# NEW (Formulario de creación para una marca específica)
# =====================
@views.route("/admin/brands/<int:brand_id>/brand-models/new", methods=["GET"])
@only_logged
def new(brand_id):

  # Obtenemos la información de la marca para contexto visual
  response = BrandModelService.fetch_by_brand(brand_id, page=1, per_page=1)

  if not response["success"]:
    flash(response["message"], "danger")
    return redirect("/admin/brands")

  return render_template(
    "brand_models/new.html",
    locals={
      "title": "Nuevo Modelo de Marca",
      "nav_link": "master-data",
      "brand": response["data"]["brand"]
    }
  )


# =====================
# CREATE
# =====================
@views.route("/admin/brands/<int:brand_id>/brand-models", methods=["POST"])
@only_logged
def create(brand_id):

  response = BrandModelService.create({
    "brand_id": brand_id,
    "name": request.form.get("name"),
    "description": request.form.get("description")
  })

  if response["success"]:
    flash(response["message"], "success")
  else:
    flash(response["message"], "danger")

  return redirect(f"/admin/brands/{brand_id}/edit")


# =====================
# EDIT
# =====================
@views.route("/admin/brands/<int:brand_id>/brand-models/<int:brand_model_id>/edit", methods=["GET"])
@only_logged
def edit(brand_id, brand_model_id):

  response = BrandModelService.fetch_one(brand_model_id)

  if not response["success"]:
    flash(response["message"], "danger")
    return redirect(f"/admin/brands/{brand_id}/edit")

  model_data = response["data"]

  # Validar que el modelo pertenezca a la marca de la URL
  if model_data["brand_id"] != brand_id:
    flash("El modelo no pertenece a la marca especificada.", "danger")
    return redirect(f"/admin/brands/{brand_id}/edit")

  return render_template(
    "brand_models/edit.html",
    locals={
      "title": "Editar Modelo de Marca",
      "nav_link": "master-data",
      "brand_model": model_data,
      "brand": model_data.get("brand")
    }
  )


# =====================
# UPDATE
# =====================
@views.route("/admin/brands/<int:brand_id>/brand-models/<int:brand_model_id>/update", methods=["POST"])
@only_logged
def update(brand_id, brand_model_id):

  response = BrandModelService.update(
    brand_model_id,
    {
      "name": request.form.get("name"),
      "description": request.form.get("description")
    }
  )

  if response["success"]:
    flash(response["message"], "success")
  else:
    flash(response["message"], "danger")

  return redirect(f"/admin/brands/{brand_id}/edit")


# =====================
# DELETE
# =====================
@views.route("/admin/brands/<int:brand_id>/brand-models/<int:brand_model_id>/delete", methods=["GET"])
@only_logged
def delete(brand_id, brand_model_id):

  response = BrandModelService.delete(brand_model_id)

  if response["success"]:
    flash(response["message"], "success")
  else:
    flash(response["message"], "danger")

  return redirect(f"/admin/brands/{brand_id}/edit")