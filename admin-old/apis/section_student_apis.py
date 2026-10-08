# admin/apis/section_student_apis.py

from flask import Blueprint, request, jsonify

from admin.configs.middlewares import only_logged
from main.application import csrf
from admin.services.section_student_service import SectionStudentService

apis = Blueprint(
  "section-student-apis",
  __name__,
  template_folder="../templates"
)


@apis.route("/api/v1/section-students/associate", methods=["POST"])
@csrf.exempt
def associate():
  data = request.get_json()

  result = SectionStudentService.create({
    "section_id": data.get("section_id"),
    "student_id": data.get("student_id")
  })

  return jsonify(result), 200


@apis.route("/api/v1/section-students/<int:relation_id>", methods=["DELETE"])
@csrf.exempt
def unassociate(relation_id):
  result = SectionStudentService.delete(relation_id)

  return jsonify(result), 200