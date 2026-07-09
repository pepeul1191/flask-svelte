# admin/views/students_views.py

from admin.services.representative_student_role_service import RepresentativeStudentRoleService
from flask import Blueprint, flash, render_template, request, redirect

from admin.configs.middlewares import only_logged
from admin.services.person_service import PersonService
from admin.services.student_service import StudentService
from admin.services.sex_service import SexService
from admin.services.document_type_service import DocumentTypeService
from admin.services.representative_role_service import RepresentativeRoleService


views = Blueprint(
  "admin-students-views",
  __name__,
  template_folder="../templates"
)


# =====================
# INDEX (LIST + SEARCH + PAGINATION)
# =====================
@views.route("/admin/students", methods=["GET"])
@only_logged
def index():

  page = request.args.get("page", default=1, type=int)
  per_page = request.args.get("per_page", default=10, type=int)

  # Filtros
  names = request.args.get("names", default="")
  last_names = request.args.get("last_names", default="")
  dni = request.args.get("dni", default="")
  code = request.args.get("code", default="")
  email = request.args.get("email", default="")

  if page < 1:
    page = 1

  if per_page < 1:
    per_page = 10

  response = StudentService.fetch_all(
    page=page,
    per_page=per_page,
    names=names,
    last_names=last_names,
    dni=dni,
    code=code,
    email=email
  )

  students = []

  pagination = {
    "page": page,
    "per_page": per_page,
    "total_students": 0,
    "total_pages": 0,
    "start_record": 0,
    "end_record": 0
  }

  # Filtros para el template
  filters = {
    "names": names,
    "last_names": last_names,
    "dni": dni,
    "code": code,
    "email": email
  }

  if response["success"]:
    students = response["data"]["students"]
    pagination = response["data"]["pagination"]
  else:
    flash(response["message"], "danger")

  return render_template(
    "students/index.html",
    locals={
      "title": "Estudiantes",
      "nav_link": "student-management",
      "students": students,
      "pagination": pagination,
      "filters": filters
    }
  )


# =====================
# NEW
# =====================
@views.route("/admin/students/new", methods=["GET"])
@only_logged
def new():
  sexes_response = SexService.fetch_all()
  document_types_response = DocumentTypeService.fetch_all()

  sexes = []
  document_types = []

  if sexes_response["success"]:
    sexes = sexes_response["data"]
  else:
    flash(sexes_response["message"], "danger")

  if document_types_response["success"]:
    document_types = document_types_response["data"]
  else:
    flash(document_types_response["message"], "danger")

  return render_template(
    "students/new.html",
    locals={
      "title": "Nuevo Estudiante",
      "nav_link": "student-management",
      "sexes": sexes,
      "document_types": document_types,
      "entity": "students"
    }
  )


# =====================
# CREATE STUDENT FROM PERSON
# =====================
@views.route("/admin/students/personal", methods=["POST"])
@only_logged
def create():

  # 1. Crear la persona en PersonService
  person_response = PersonService.create({
    "names": request.form.get("names"),
    "last_names": request.form.get("last_names"),
    "document_type_id": request.form.get("document_type_id"),
    "document_number": request.form.get("document_number"),
    "sex_id": request.form.get("sex_id"),
    "birth_date": request.form.get("birth_date"),
    "image_url": request.form.get("image_url")
  })

  if not person_response["success"]:
    flash(person_response["message"], "danger")
    return redirect("/admin/students/new")

  # 2. Con el id de la persona creada, se genera el registro del estudiante
  person_id = person_response["data"]["id"]
  student_response = StudentService.create({
    "code": request.form.get("document_number"),
    "email": request.form.get("email"),
    "person_id": person_id,
    "user_id": request.form.get("user_id")  # Opcional, puede venir del formulario
  })

  if student_response["success"]:
    flash(student_response["message"], "success")
    student_id = student_response["data"]["id"]
    return redirect(f"/admin/students/{student_id}/edit")

  flash(student_response["message"], "danger")
  return redirect("/admin/students/new")


# =====================
# EDIT
# =====================
@views.route("/admin/students/<int:student_id>/edit", methods=["GET"])
@only_logged
def edit(student_id):

  response = StudentService.fetch_one(student_id)

  sexes_response = SexService.fetch_all()
  document_types_response = DocumentTypeService.fetch_all()

  if not response["success"]:
    flash(response["message"], "danger")
    return redirect("/admin/students")
  
  sexes = []
  document_types = []

  if sexes_response["success"]:
    sexes = sexes_response["data"]
  else:
    flash(sexes_response["message"], "danger")

  if document_types_response["success"]:
    document_types = document_types_response["data"]
  else:
    flash(document_types_response["message"], "danger")

  return render_template(
    "students/edit.html",
    locals={
      "title": "Editar Estudiante",
      "nav_link": "student-management",
      "record": response["data"],
      "person": response["data"]["person"],
      "sexes": sexes,
      "document_types": document_types,
      "entity": "students"
    }
  )


# =====================
# UPDATE PERSON
# =====================
@views.route("/admin/students/personal/<int:person_id>/edit", methods=["POST"])
@only_logged
def edit_personal(person_id):

  response = PersonService.update(person_id, {
    "names": request.form.get("names"),
    "last_names": request.form.get("last_names"),
    "document_type_id": request.form.get("document_type_id"),
    "document_number": request.form.get("document_number"),
    "sex_id": request.form.get("sex_id"),
    "birth_date": request.form.get("birth_date"),
    "image_url": request.form.get("image_url")
  })

  if response["success"]:
    # Buscamos el estudiante asociado a esa persona usando StudentService
    student_response = StudentService.fetch_by_person_id(person_id)
    
    if student_response["success"]:
      flash(response["message"], "success")
      student_id = student_response["data"]["id"]
      return redirect(f"/admin/students/{student_id}/edit")
    
    # En caso de que la persona se actualice pero no se encuentre su Student
    flash("Persona actualizada, pero no se encontró el estudiante asociado.", "warning")
    return redirect(request.referrer)

  flash(response["message"], "danger")
  return redirect(request.referrer)


# =====================
# UPDATE STUDENT
# =====================
@views.route("/admin/students/<int:student_id>/edit", methods=["POST"])
@only_logged
def edit_student(student_id):

  response = StudentService.update(student_id, {
    "code": request.form.get("code"),
    "email": request.form.get("email"),
    "user_id": request.form.get("user_id"),
  })

  if response["success"]:
    flash("Estudiante actualizado.", "success")
    return redirect(f"/admin/students/{student_id}/edit")

  flash(response["message"], "danger")
  return redirect(request.referrer)


# =====================
# DELETE
# =====================
@views.route(
  "/admin/students/<int:student_id>/delete",
  methods=["GET"]
)
@only_logged
def delete(student_id):

  response = StudentService.delete(student_id)

  if response["success"]:
    flash(response["message"], "success")
  else:
    flash(response["message"], "danger")

  return redirect("/admin/students")


# =====================
# SHOW STUDENT REPRESENTATIVES
# =====================
@views.route("/admin/students/<int:student_id>/representatives", methods=["GET"])
@only_logged
def show_representatives(student_id):
  page = request.args.get("page", default=1, type=int)
  per_page = request.args.get("per_page", default=10, type=int)

  names = request.args.get("names", default="")
  last_names = request.args.get("last_names", default="")
  dni = request.args.get("dni", default="")
  email = request.args.get("email", default="")
  related = request.args.get("related", default="related")

  student_response = StudentService.fetch_one(student_id)

  representative_roles_response = RepresentativeRoleService.fetch_all()

  if page < 1:
    page = 1

  if per_page < 1:
    per_page = 10

  response = RepresentativeStudentRoleService.fetch_by_student(
    page=page,
    per_page=per_page,
    names=names,
    last_names=last_names,
    dni=dni,
    email=email,
    related=related,
    student_id=student_id,
  )

  representatives = []

  pagination = {
    "page": page,
    "per_page": per_page,
    "total_representatives": 0,
    "total_pages": 0,
    "start_record": 0,
    "end_record": 0
  }

  filters = {
    "names": names,
    "last_names": last_names,
    "dni": dni,
    "email": email,
    "related": related
  }

  if response["success"]:
    representatives = response["data"]["representatives"]
    pagination = response["data"]["pagination"]
  else:
    flash(response["message"], "danger")

  if not student_response["success"]:
    flash(student_response["message"], "danger")
    return redirect("/admin/students")

  # print(representatives)
  # print(representative_roles_response["data"])

  return render_template(
    "students/representatives.html",
    locals={
      "title": "Apoderados del Estudiante",
      "nav_link": "student-management",
      "representatives": representatives,
      "pagination": pagination,
      "representative_roles": representative_roles_response["data"],
      "filters": filters,
      "record": student_response["data"]
    }
  )