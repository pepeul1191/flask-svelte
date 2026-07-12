# admin/views/level.py

from flask import Blueprint, flash, render_template, request, redirect

from admin.configs.middlewares import only_logged
from admin.services.level_service import LevelService
from admin.services.courses_service import CourseService

views = Blueprint(
  "admin-levels-views",
  __name__,
  template_folder="../templates"
)


# =====================
# INDEX (LIST + SEARCH + PAGINATION)
# =====================
@views.route("/admin/levels", methods=["GET"])
@only_logged
def index():

  page = request.args.get("page", default=1, type=int)
  per_page = request.args.get("per_page", default=10, type=int)
  search_query = request.args.get("name", default='')

  if page < 1:
    page = 1

  if per_page < 1:
    per_page = 10

  response = LevelService.fetch_all(
    page=page,
    per_page=per_page,
    search_query=search_query
  )

  levels = []
  pagination = {
    "page": page,
    "per_page": per_page,
    "total_levels": 0,
    "total_pages": 0,
    "start_record": 0,
    "end_record": 0
  }

  if response["success"]:
    levels = response["data"]["levels"]
    pagination = response["data"]["pagination"]
  else:
    flash(response["message"], "danger")

  return render_template(
    "levels/index.html",
    locals={
      "title": "Niveles",
      "nav_link": "academic-management",
      "levels": levels,
      "pagination": pagination,
      "search_query": search_query
    }
  )


# =====================
# NEW
# =====================
@views.route("/admin/levels/new", methods=["GET"])
@only_logged
def new():

  return render_template(
    "levels/new.html",
    locals={
      "title": "Nuevo Nivel",
      "nav_link": "academic-management"
    }
  )


# =====================
# CREATE
# =====================
@views.route("/admin/levels", methods=["POST"])
@only_logged
def create():

  response = LevelService.create({
    "name": request.form.get("name")
  })

  if response["success"]:
    flash(response["message"], "success")
    return redirect("/admin/levels")

  flash(response["message"], "danger")
  return redirect("/admin/levels/new")


# =====================
# EDIT
# =====================
@views.route("/admin/levels/<int:level_id>/edit", methods=["GET"])
@only_logged
def edit(level_id):

  response = LevelService.fetch_one(level_id)
  response_courses = CourseService.fetch_by_level(level_id=level_id)

  if not response["success"]:
    flash(response["message"], "danger")
    return redirect("/admin/levels")

  return render_template(
    "levels/edit.html",
    locals={
      "title": "Editar Nivel",
      "nav_link": "academic-management",
      "level": response["data"],
      "courses": response_courses["data"]["courses"]
    }
  )


# =====================
# UPDATE
# =====================
@views.route("/admin/levels/<int:level_id>/update", methods=["POST"])
@only_logged
def update(level_id):

  response = LevelService.update(
    level_id,
    {"name": request.form.get("name")}
  )

  if response["success"]:
    flash(response["message"], "success")
  else:
    flash(response["message"], "danger")

  return redirect(f"/admin/levels/{level_id}/edit")


# =====================
# DELETE
# =====================
@views.route("/admin/levels/<int:level_id>/delete", methods=["GET"])
@only_logged
def delete(level_id):

  response = LevelService.delete(level_id)

  if response["success"]:
    flash(response["message"], "success")
  else:
    flash(response["message"], "danger")

  return redirect("/admin/levels")