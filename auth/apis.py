# auth/apis.py
from flask import Blueprint, jsonify

apis = Blueprint('auth-apis', __name__)

@apis.route('/api/v1/demo', methods=['GET'])
def demo_get():
  return jsonify({
      'message': 'hola GET'
    }), 200

@apis.route('/api/v1/demo', methods=['POST'])
def demo_post():
  return jsonify({
      'message': 'hola POST'
    }), 200
