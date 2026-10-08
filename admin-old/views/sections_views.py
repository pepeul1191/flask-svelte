# admin/views/sections_views.py
from flask import Blueprint, flash, render_template, request, redirect, url_for

from admin.configs.middlewares import only_logged
from admin.services.courses_service import CourseService
from admin.services.section_service import SectionService
from admin.services.level_service import LevelService

views = Blueprint(
  "admin-sections-views",
  __name__,
  template_folder="../templates"
)


# =====================
# INDEX (LIST + SEARCH + PAGINATION)
# =====================
@views.route("/admin/levels/<int:level_id>/courses/<int:course_id>/sections", methods=["GET"])
@only_logged
def index(level_id, course_id):

  # Verificar que el nivel existe
  level_response = LevelService.fetch_one(level_id)
  if not level_response["success"]:
    flash(level_response["message"], "danger")
    return redirect("/admin/levels")

  # Verificar que el curso existe
  course_response = CourseService.fetch_one(level_id, course_id)
  if not course_response["success"]:
    flash(course_response["message"], "danger")
    return redirect(f"/admin/levels/{level_id}/courses")

  page = request.args.get("page", default=1, type=int)
  per_page = request.args.get("per_page", default=10, type=int)
  search_query = request.args.get("search", default='')

  if page < 1:
    page = 1

  if per_page < 1:
    per_page = 10

  response = SectionService.fetch_by_course(
    course_id=course_id,
    page=page,
    per_page=per_page,
    search_query=search_query
  )

  sections = []
  pagination = {
    "page": page,
    "per_page": per_page,
    "total_sections": 0,
    "total_pages": 0,
    "start_record": 0,
    "end_record": 0
  }
  course = {}

  if response["success"]:
    sections = response["data"]["sections"]
    pagination = response["data"]["pagination"]
    course = response["data"]["course"]
  else:
    flash(response["message"], "danger")

  return render_template(
    "sections/index.html",
    locals={
      "title": "Secciones",
      "nav_link": "academic-management",
      "level_id": level_id,
      "course_id": course_id,
      "level": level_response["data"],
      "course": course,
      "sections": sections,
      "pagination": pagination,
      "search_query": search_query
    }
  )


# =====================
# NEW
# =====================
@views.route("/admin/levels/<int:level_id>/courses/<int:course_id>/sections/new", methods=["GET"])
@only_logged
def new(level_id, course_id):

  # Verificar que el nivel existe
  level_response = LevelService.fetch_one(level_id)
  if not level_response["success"]:
    flash(level_response["message"], "danger")
    return redirect("/admin/levels")

  # Verificar que el curso existe
  course_response = CourseService.fetch_one(level_id, course_id)
  if not course_response["success"]:
    flash(course_response["message"], "danger")
    return redirect(f"/admin/levels/{level_id}/courses")

  return render_template(
    "sections/new.html",
    locals={
      "title": "Nueva Sección",
      "nav_link": "academic-management",
      "level_id": level_id,
      "course_id": course_id,
      "level": level_response["data"],
      "course": course_response["data"]
    }
  )


# =====================
# CREATE
# =====================
@views.route("/admin/levels/<int:level_id>/courses/<int:course_id>/sections", methods=["POST"])
@only_logged
def create(level_id, course_id):

  response = SectionService.create(course_id, {
    "name": request.form.get("name"),
    "code": request.form.get("code"),
    "description": request.form.get("description"),
    "image_url": request.form.get("image_url"),
  })

  if response["success"]:
    flash(response["message"], "success")
    return redirect(f"/admin/levels/{level_id}/courses/{course_id}/sections/{response['data']['id']}/edit")

  flash(response["message"], "danger")
  return redirect(f"/admin/levels/{level_id}/courses/{course_id}/sections/new")


# =====================
# EDIT
# =====================
@views.route("/admin/levels/<int:level_id>/courses/<int:course_id>/sections/<int:section_id>/edit", methods=["GET"])
@only_logged
def edit(level_id, course_id, section_id):
  
  # Verificar que el nivel existe
  level_response = LevelService.fetch_one(level_id)
  if not level_response["success"]:
    flash(level_response["message"], "danger")
    return redirect("/admin/levels")

  # Verificar que el curso existe
  course_response = CourseService.fetch_one(level_id, course_id)
  if not course_response["success"]:
    flash(course_response["message"], "danger")
    return redirect(f"/admin/levels/{level_id}/courses")

  response = SectionService.fetch_one(course_id, section_id)

  if not response["success"]:
    flash(response["message"], "danger")
    return redirect(f"/admin/levels/{level_id}/courses/{course_id}/sections")

  return render_template(
    "sections/edit.html",
    locals={
      "title": "Editar Sección",
      "nav_link": "academic-management",
      "level_id": level_id,
      "course_id": course_id,
      "section_id": section_id,
      "level": level_response["data"],
      "course": course_response["data"],
      "section": response["data"]
    }
  )


# =====================
# UPDATE
# =====================
@views.route("/admin/levels/<int:level_id>/courses/<int:course_id>/sections/<int:section_id>/update", methods=["POST"])
@only_logged
def update(level_id, course_id, section_id):

  response = SectionService.update(
    course_id,
    section_id,
    {
      "name": request.form.get("name"),
      "code": request.form.get("code"),
      "description": request.form.get("description"),
      "image_url": request.form.get("image_url"),
    }
  )

  if response["success"]:
    flash(response["message"], "success")
  else:
    flash(response["message"], "danger")

  return redirect(f"/admin/levels/{level_id}/courses/{course_id}/sections/{section_id}/edit")


# =====================
# DELETE
# =====================
@views.route("/admin/levels/<int:level_id>/courses/<int:course_id>/sections/<int:section_id>/delete", methods=["GET"])
@only_logged
def delete(level_id, course_id, section_id):

  response = SectionService.delete(course_id, section_id)

  if response["success"]:
    flash(response["message"], "success")
  else:
    flash(response["message"], "danger")

  return redirect(f"/admin/levels/{level_id}/courses/{course_id}/edit")