# admin/apis/representative_student_role_apis.py

from flask import Blueprint, request, jsonify

from admin.configs.middlewares import only_logged
from admin.services.representative_student_role_service import (
  RepresentativeStudentRoleService
)

apis = Blueprint(
  "representative-student-role-apis",
  __name__,
  template_folder="../templates"
)


@apis.route("/api/v1/student-representatives/associate", methods=["POST"])
@only_logged
def associate():

  data = request.get_json()

  result = RepresentativeStudentRoleService.create({
    "student_id": data.get("student_id"),
    "representative_id": data.get("representative_id"),
    "representative_role_id": data.get("representative_role_id")
  })

  return jsonify(result), 200


@apis.route("/api/v1/student-representatives/<int:relation_id>", methods=["DELETE"])
@only_logged
def unassociate(relation_id):

  result = RepresentativeStudentRoleService.delete(relation_id)

  return jsonify(result), 200


@apis.route("/api/v1/student-representatives/<int:relation_id>/role", methods=["PUT"])
@only_logged
def update_role(relation_id):

  data = request.get_json()

  result = RepresentativeStudentRoleService.update_role(
    relation_id,
    data.get("representative_role_id")
  )

  return jsonify(result), 200