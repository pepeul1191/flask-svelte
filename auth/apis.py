# auth/apis.py
from flask import Blueprint

apis = Blueprint('auth-apis', __name__)

@apis.route('/api/v1/demo', methods=['GET'])
def demo():
  return 'hola mundo', 200
