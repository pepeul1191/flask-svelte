# admin/views/representative.py

from flask import Blueprint, flash, render_template, request, redirect

from admin.configs.middlewares import only_logged
from admin.services.person_service import PersonService
from admin.services.representative_service import RepresentativeService
from admin.services.sex_service import SexService
from admin.services.document_type_service import DocumentTypeService
from admin.services.representative_student_role_service import RepresentativeStudentRoleService
from admin.services.representative_role_service import RepresentativeRoleService

views = Blueprint(
  "admin-representatives-views",
  __name__,
  template_folder="../templates"
)


# =====================
# INDEX
# =====================
@views.route("/admin/representatives", methods=["GET"])
@only_logged
def index():

  page = request.args.get("page", default=1, type=int)
  per_page = request.args.get("per_page", default=10, type=int)

  names = request.args.get("names", default="")
  last_names = request.args.get("last_names", default="")
  dni = request.args.get("dni", default="")
  email = request.args.get("email", default="")

  if page < 1:
    page = 1

  if per_page < 1:
    per_page = 10

  response = RepresentativeService.fetch_all(
    page=page,
    per_page=per_page,
    names=names,
    last_names=last_names,
    dni=dni,
    email=email
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
    "email": email
  }

  if response["success"]:
    representatives = response["data"]["representatives"]
    pagination = response["data"]["pagination"]
  else:
    flash(response["message"], "danger")

  return render_template(
    "representatives/index.html",
    locals={
      "title": "Representantes",
      "nav_link": "representative-management",
      "representatives": representatives,
      "pagination": pagination,
      "filters": filters
    }
  )


# =====================
# NEW
# =====================
@views.route("/admin/representatives/new", methods=["GET"])
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
    "representatives/new.html",
    locals={
      "title": "Nuevo Representante",
      "nav_link": "representative-management",
      "sexes": sexes,
      "document_types": document_types,
      "entity": "representatives"
    }
  )


# =====================
# CREATE
# =====================
@views.route("/admin/representatives/personal", methods=["POST"])
@only_logged
def create():

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
    return redirect("/admin/representatives/new")

  person_id = person_response["data"]["id"]

  representative_response = RepresentativeService.create({
    "email": request.form.get("email"),
    "user_id": request.form.get("user_id"),
    "person_id": person_id
  })

  if representative_response["success"]:
    flash(representative_response["message"], "success")
    representative_id = representative_response["data"]["id"]
    return redirect(
      f"/admin/representatives/{representative_id}/edit"
    )

  flash(representative_response["message"], "danger")
  return redirect("/admin/representatives/new")


# =====================
# EDIT
# =====================
@views.route(
  "/admin/representatives/<int:representative_id>/edit",
  methods=["GET"]
)
@only_logged
def edit(representative_id):

  response = RepresentativeService.fetch_one(
    representative_id
  )

  sexes_response = SexService.fetch_all()
  document_types_response = DocumentTypeService.fetch_all()
  representative_roles_response = RepresentativeStudentRoleService.fetch_by_representative(representative_id=representative_id, related="related")

  if not response["success"]:
    flash(response["message"], "danger")
    return redirect("/admin/representatives")

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

  print('1 +++++++++++++++++++++++++++++++')
  print(representative_roles_response["data"])
  print('2 +++++++++++++++++++++++++++++++')

  return render_template(
    "representatives/edit.html",
    locals={
      "title": "Editar Representante",
      "nav_link": "representative-management",
      "record": response["data"],
      "person": response["data"]["person"],
      "students": representative_roles_response["data"]["students"],
      "sexes": sexes,
      "document_types": document_types,
      "entity": "representatives"
    }
  )


# =====================
# UPDATE PERSON
# =====================
@views.route(
  "/admin/representatives/personal/<int:person_id>/edit",
  methods=["POST"]
)
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

    representative_response = (
      RepresentativeService.fetch_by_person_id(
        person_id
      )
    )

    if representative_response["success"]:
      flash(response["message"], "success")

      representative_id = (
        representative_response["data"]["id"]
      )

      return redirect(
        f"/admin/representatives/{representative_id}/edit"
      )

    flash(
      "Persona actualizada, pero no se encontró el representante asociado.",
      "warning"
    )

    return redirect(request.referrer)

  flash(response["message"], "danger")
  return redirect(request.referrer)


# =====================
# UPDATE REPRESENTATIVE
# =====================
@views.route(
  "/admin/representatives/<int:representative_id>/edit",
  methods=["POST"]
)
@only_logged
def edit_representative(representative_id):

  response = RepresentativeService.update(
    representative_id,
    {
      "email": request.form.get("email"),
      "user_id": request.form.get("user_id")
    }
  )

  if response["success"]:
    flash("Representante actualizado.", "success")
    return redirect(
      f"/admin/representatives/{representative_id}/edit"
    )

  flash(response["message"], "danger")
  return redirect(request.referrer)


# =====================
# DELETE
# =====================
@views.route(
  "/admin/representatives/<int:representative_id>/delete",
  methods=["GET"]
)
@only_logged
def delete(representative_id):

  response = RepresentativeService.delete(
    representative_id
  )

  if response["success"]:
    flash(response["message"], "success")
  else:
    flash(response["message"], "danger")

  return redirect("/admin/representatives")

# =====================
# SHOW REPRESENTATIVE STUDENTS
# =====================
@views.route("/admin/representatives/<int:representative_id>/students", methods=["GET"])
@only_logged
def show_students(representative_id):
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)

    code = request.args.get("code", default="")
    names = request.args.get("names", default="")
    last_names = request.args.get("last_names", default="")
    dni = request.args.get("dni", default="")
    email = request.args.get("email", default="")
    related = request.args.get("related", default="related")

    representative_roles_response = RepresentativeRoleService.fetch_all()
    representative_roles = representative_roles_response["data"] if representative_roles_response["success"] else []

    representative_response = RepresentativeService.fetch_one(representative_id)

    if page < 1:
        page = 1

    if per_page < 1:
        per_page = 10

    response = RepresentativeStudentRoleService.fetch_by_representative(
        page=page,
        per_page=per_page,
        code=code,
        names=names,
        last_names=last_names,
        dni=dni,
        email=email,
        related=related,
        representative_id=representative_id,
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

    filters = {
        "code": code,
        "names": names,
        "last_names": last_names,
        "dni": dni,
        "email": email,
        "related": related
    }

    if response["success"]:
        students = response["data"]["students"]
        pagination = response["data"]["pagination"]
    else:
        flash(response["message"], "danger")

    if not representative_response["success"]:
        flash(representative_response["message"], "danger")
        return redirect("/admin/representatives")

    return render_template(
        "representatives/students.html",
        locals={
            "title": "Estudiantes del Representante",
            "nav_link": "representative-management",
            "representative_roles": representative_roles,  # Añadir esta línea
            "students": students,
            "pagination": pagination,
            "filters": filters,
            "record": representative_response["data"]
        }
    )