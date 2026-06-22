# auth/apis.py
from flask import Blueprint, jsonify, session

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

@apis.route('/api/v1/session', methods=['GET'])
def get_session():
  user = session.get('user')

  if not user:
    return jsonify({
      'success': False,
      'message': 'No hay sesión activa'
    }), 401

  return jsonify({
    'success': True,
    'data': {
      'user': session.get('user'),
      'roles': session.get('roles', []),
      'tokens': session.get('tokens', {})
    }
  }), 200