# admin/apis/students_apis.py
from flask import Blueprint, jsonify

from main.application import csrf
from admin.services.student_service import StudentService
from main.services import ApplicationService


apis = Blueprint(
  "students-apis",
  __name__
)


@apis.route("/api/v1/students/<int:student_id>", methods=["GET"])
@csrf.exempt
def fetch_one(student_id):

  try:
    result = StudentService.fetch_one(
      student_id
    )

    status_code = 200

    if result.get("success") is False:
      if result.get("message") == "Estudiante no encontrado":
        status_code = 404
      else:
        status_code = 400

    return jsonify(result), status_code

  except Exception as e:
    result = ApplicationService.handle_error(
      "Error al obtener estudiante",
      str(e)
    )

    return jsonify(result), 500