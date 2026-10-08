# admin/apis/workers_apis.py

from flask import Blueprint, jsonify, request

from main.application import csrf
from admin.services.worker_service import WorkerService
from main.services import ApplicationService

apis = Blueprint('admin-workers-apis', __name__, template_folder='../templates')


@apis.route('/api/v1/workers', methods=["GET"])
@csrf.exempt
def search():
  try:
    # Obtener el parámetro 'name' de la query string
    name = request.args.get('name', '').strip()
    
    # Si no hay nombre o es muy corto, retornar lista vacía
    if not name or len(name) < 2:
      return jsonify({
        'data': [],
        'message': 'Se requiere al menos 2 caracteres para buscar',
        'total': 0
      }), 200
    
    # Buscar workers por nombre
    result = WorkerService.search_by_name(name)
    
    status_code = 200
    
    if result.get("success") is False:
      if result.get("message") == "Worker no encontrado":
        status_code = 404
      else:
        status_code = 400
    
    return jsonify(result), status_code
    
  except Exception as e:
    result = ApplicationService.handle_error(
      "Error al buscar workers",
      str(e)
    )
    
    return jsonify(result), 500


@apis.route('/api/v1/workers/<int:worker_id>', methods=["GET"])
@csrf.exempt
def fetch_one(worker_id):
  try:
    result = WorkerService.fetch_one(worker_id)
    
    status_code = 200
    
    if result.get("success") is False:
      if result.get("message") == "Worker no encontrado":
        status_code = 404
      else:
        status_code = 400
    
    return jsonify(result), status_code
    
  except Exception as e:
    result = ApplicationService.handle_error(
      "Error al obtener worker",
      str(e)
    )
    
    return jsonify(result), 500