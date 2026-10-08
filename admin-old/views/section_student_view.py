# admin/views/section_student_view.py

from flask import Blueprint, flash, render_template, request, redirect
from admin.configs.middlewares import only_logged
from admin.services.section_student_service import SectionStudentService
from admin.services.section_service import SectionService
from admin.services.student_service import StudentService

views = Blueprint(
  "admin-section-students-views",
  __name__,
  template_folder="../templates"
)


# =========================
# LISTAR ESTUDIANTES
# =========================
@views.route(
  "/admin/levels/<int:level_id>/courses/<int:course_id>/sections/<int:section_id>/students",
  methods=["GET"]
)
@only_logged
def index(level_id, course_id, section_id):
  # Obtener filtros de la URL
  filters = {
    "names": request.args.get("names", ""),
    "last_names": request.args.get("last_names", ""),
    "code": request.args.get("code", ""),
    "email": request.args.get("email", ""),
    "related": request.args.get("related", "all"),
    "page": int(request.args.get("page", 1)),
    "per_page": int(request.args.get("per_page", 10))
  }

  response = SectionStudentService.fetch_by_section(
    section_id,
    related=filters["related"],
    page=filters["page"],
    per_page=filters["per_page"],
    code=filters["code"],
    email=filters["email"],
    names=filters["names"],
    last_names=filters["last_names"],
  )

  students = []
  pagination = None

  if response["success"]:
    students = response["data"]["students"]
    pagination = response["data"]["pagination"]
  else:
    flash(response["message"], "danger")

  section_response = SectionService.fetch_one(course_id, section_id)

  locals = {
    "title": "Estudiantes de la sección",
    "nav_link": "academic-management",
    "level_id": level_id,
    "course_id": course_id,
    "section_id": section_id,
    "section": section_response["data"] if section_response["success"] else None,
    "students": students,
    "pagination": pagination,
    "filters": filters
  }

  return render_template("sections/students.html", locals=locals)