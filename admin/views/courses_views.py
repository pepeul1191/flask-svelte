# admin/views/courses_views.py

from flask import Blueprint, flash, render_template, request, redirect, url_for

from admin.configs.middlewares import only_logged
from admin.services.courses_service import CourseService
from admin.services.level_service import LevelService
from admin.services.worker_service import WorkerService

views = Blueprint(
  "admin-courses-views",
  __name__,
  template_folder="../templates"
)


# =====================
# INDEX (LIST + SEARCH + PAGINATION)
# =====================
@views.route("/admin/levels/<int:level_id>/courses", methods=["GET"])
@only_logged
def index(level_id):

  # Verificar que el nivel existe
  level_response = LevelService.fetch_one(level_id)
  if not level_response["success"]:
    flash(level_response["message"], "danger")
    return redirect("/admin/levels")

  page = request.args.get("page", default=1, type=int)
  per_page = request.args.get("per_page", default=10, type=int)
  search_query = request.args.get("search", default='')

  if page < 1:
    page = 1

  if per_page < 1:
    per_page = 10

  response = CourseService.fetch_by_level(
    level_id=level_id,
    page=page,
    per_page=per_page,
    search_query=search_query
  )

  courses = []
  pagination = {
    "page": page,
    "per_page": per_page,
    "total_courses": 0,
    "total_pages": 0,
    "start_record": 0,
    "end_record": 0
  }
  level = {}

  if response["success"]:
    courses = response["data"]["courses"]
    pagination = response["data"]["pagination"]
    level = response["data"]["level"]
  else:
    flash(response["message"], "danger")

  return render_template(
    "courses/index.html",
    locals={
      "title": "Cursos",
      "nav_link": "academic-management",
      "level_id": level_id,
      "level": level,
      "courses": courses,
      "pagination": pagination,
      "search_query": search_query
    }
  )


# =====================
# NEW
# =====================
@views.route("/admin/levels/<int:level_id>/courses/new", methods=["GET"])
@only_logged
def new(level_id):

  # Verificar que el nivel existe
  level_response = LevelService.fetch_one(level_id)
  if not level_response["success"]:
    flash(level_response["message"], "danger")
    return redirect("/admin/levels")

  return render_template(
    "courses/new.html",
    locals={
      "title": "Nuevo Curso",
      "nav_link": "academic-management",
      "level_id": level_id,
      "level": level_response["data"]
    }
  )


# =====================
# CREATE
# =====================
@views.route("/admin/levels/<int:level_id>/courses", methods=["POST"])
@only_logged
def create(level_id):

  response = CourseService.create(level_id, {
    "name": request.form.get("name"),
    "code": request.form.get("code"),
    "description": request.form.get("description"),
    "sylabus_url": request.form.get("sylabus_url"),
    "worker_id": request.form.get("worker_id")
  })

  if response["success"]:
    flash(response["message"], "success")
    return redirect(f"/admin/levels/{level_id}/courses")

  flash(response["message"], "danger")
  return redirect(f"/admin/levels/{level_id}/courses/new")


# =====================
# EDIT
# =====================
@views.route("/admin/levels/<int:level_id>/courses/<int:course_id>/edit", methods=["GET"])
@only_logged
def edit(level_id, course_id):

  # Verificar que el nivel existe
  level_response = LevelService.fetch_one(level_id)
  if not level_response["success"]:
    flash(level_response["message"], "danger")
    return redirect("/admin/levels")

  response = CourseService.fetch_one(level_id, course_id)

  if not response["success"]:
    flash(response["message"], "danger")
    return redirect(f"/admin/levels/{level_id}/courses")

  worker = None
  if(response["data"]["worker_id"]):
    response_worker = WorkerService.fetch_one(response["data"]["worker_id"])
    worker = response_worker["data"]

  return render_template(
    "courses/edit.html",
    locals={
      "title": "Editar Curso",
      "nav_link": "academic-management",
      "level_id": level_id,
      "level": level_response["data"],
      "course": response["data"],
      "worker": worker
    }
  )


# =====================
# UPDATE
# =====================
@views.route("/admin/levels/<int:level_id>/courses/<int:course_id>/update", methods=["POST"])
@only_logged
def update(level_id, course_id):

  worker_id = request.form.get("worker_id")

  response = CourseService.update(
    level_id,
    course_id,
    {
      "name": request.form.get("name"),
      "code": request.form.get("code"),
      "description": request.form.get("description"),
      "sylabus_url": request.form.get("sylabus_url"),
      "worker_id": int(worker_id) if worker_id else None,
    }
  )

  if response["success"]:
    flash(response["message"], "success")
  else:
    flash(response["message"], "danger")

  return redirect(f"/admin/levels/{level_id}/courses/{course_id}/edit")


# =====================
# DELETE
# =====================
@views.route("/admin/levels/<int:level_id>/courses/<int:course_id>/delete", methods=["GET"])
@only_logged
def delete(level_id, course_id):

  response = CourseService.delete(level_id, course_id)

  if response["success"]:
    flash(response["message"], "success")
  else:
    flash(response["message"], "danger")

  return redirect(f"/admin/levels/{level_id}/courses")