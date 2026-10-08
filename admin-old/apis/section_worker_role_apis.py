# admin/apis/section_worker_role_apis.py

from flask import Blueprint, request, jsonify

from main.application import csrf

from admin.services.section_worker_role_service import (
  SectionWorkerRoleService
)


apis = Blueprint(
  "section-worker-role-apis",
  __name__,
  template_folder="../templates"
)


# =========================
# ASOCIAR TRABAJADOR
# =========================
@apis.route(
  "/api/v1/section-workers/associate",
  methods=["POST"]
)
@csrf.exempt
def associate():

  data = request.get_json()


  result = SectionWorkerRoleService.create({

    "section_id": data.get(
      "section_id"
    ),

    "worker_id": data.get(
      "worker_id"
    ),

    "worker_role_id": data.get(
      "worker_role_id"
    )

  })


  return jsonify(result), 200



# =========================
# DESASOCIAR TRABAJADOR
# =========================
@apis.route(
  "/api/v1/section-workers/<int:relation_id>",
  methods=["DELETE"]
)
@csrf.exempt
def unassociate(
  relation_id
):

  result = SectionWorkerRoleService.delete(
    relation_id
  )


  return jsonify(result), 200



# =========================
# ACTUALIZAR ROL
# =========================
@apis.route(
  "/api/v1/section-workers/<int:relation_id>/role",
  methods=["PUT"]
)
@csrf.exempt
def update_role(
  relation_id
):

  data = request.get_json()


  result = SectionWorkerRoleService.update_role(
    relation_id,
    data.get(
      "worker_role_id"
    )
  )


  return jsonify(result), 200