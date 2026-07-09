# admin/apis/representatives_apis.py

from flask import Blueprint, jsonify

from main.application import csrf
from admin.services.representative_service import RepresentativeService
from main.services import ApplicationService


apis = Blueprint(
  "representatives-apis",
  __name__
)


@apis.route("/api/v1/representatives/<int:representative_id>", methods=["GET"])
@csrf.exempt
def fetch_one(representative_id):

  try:
    result = RepresentativeService.fetch_one(
      representative_id
    )

    status_code = 200

    if result.get("success") is False:
      if result.get("message") == "Representante no encontrado":
        status_code = 404
      else:
        status_code = 400

    return jsonify(result), status_code

  except Exception as e:
    result = ApplicationService.handle_error(
      "Error al obtener representante",
      str(e)
    )

    return jsonify(result), 500