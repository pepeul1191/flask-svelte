# admin/apis/districts_apis.py

from flask import Blueprint, jsonify, request

from admin.configs.middlewares import only_logged
from admin.services.district_service import DistrictService

apis = Blueprint('admin-index-apis', __name__, template_folder='../templates')

@apis.route('/api/v1/districts', methods=["GET"])
@only_logged
def search():
  # Obtener el parámetro 'name' de la query string
  name = request.args.get('name', '').strip()
  
  # Si no hay nombre o es muy corto, retornar lista vacía
  if not name or len(name) < 2:
    return jsonify({
      'data': [],
      'message': 'Se requiere al menos 2 caracteres para buscar',
      'total': 0
    }), 200
  
  # Buscar ubicaciones por nombre
  result = DistrictService.search_by_name(name)
  
  # Retornar respuesta JSON
  return jsonify(result), 200