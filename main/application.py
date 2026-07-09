# main/application.py
from flask import Flask, jsonify, flash
from flask_jwt_extended import JWTManager
from flask_session import Session
from flask_wtf.csrf import CSRFProtect, CSRFError
from main.middlewares import set_global_headers
from main.constants import ENV

from flask import Blueprint, flash, redirect, render_template, request, session


APP = Flask(
  __name__,
  static_folder='../static',
  static_url_path='/',
  #template_folder='../templates'
)

APP.config['SECRET_KEY'] = 'your_secret_key'
APP.config['SESSION_TYPE'] = 'filesystem'
APP.config['SESSION_PERMANENT'] = False
APP.config['SESSION_USE_SIGNER'] = True
APP.config['SESSION_KEY_PREFIX'] = 'session:'
APP.config['JWT_SECRET_KEY'] = 'tu_clave_secreta_aqui' 

APP.config.update(ENV)

APP.after_request(set_global_headers)

csrf = CSRFProtect(APP)

Session(APP)

jwt = JWTManager(APP)

REVOKED_TOKENS = []

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
  jti = jwt_payload['jti']
  return jti in REVOKED_TOKENS

@jwt.unauthorized_loader
def unauthorized_response(callback):
  return jsonify({"error": "Acceso no autorizado. Debes proporcionar un token válido."}), 401

@jwt.expired_token_loader
def expired_token_response(jwt_header, jwt_payload):
  return jsonify({"error": "El token ha expirado. Por favor, inicia sesión nuevamente."}), 401

@jwt.invalid_token_loader
def invalid_token_response(reason):
  return jsonify({"error": "Token inválido o corrupto. Revisa tu autenticación."}), 401

@jwt.needs_fresh_token_loader
def needs_fresh_token_response(jwt_header, jwt_payload):
  return jsonify({"error": "Se requiere un token fresco. Vuelve a iniciar sesión."}), 401

@APP.errorhandler(CSRFError)
def handle_csrf_error(e):
  reason = e.description.lower()

  if "expired" in reason:
    flash("La sesión ha expirado. Por favor inicia sesión nuevamente.", "danger")
    return redirect("/sign-in")

  if "missing" in reason:
    flash("Falta el token CSRF. Intenta enviar nuevamente el formulario.", "danger")
    return redirect(request.referrer or "/")

  flash("Error de validación CSRF.", "danger")
  return redirect(request.referrer or "/")

@APP.route("/api/routes", methods=["GET"])
def show_routes():
  routes = []

  for rule in APP.url_map.iter_rules():
    routes.append({
      "endpoint": rule.endpoint,
      "route": str(rule),
      "methods": list(rule.methods)
    })

  return jsonify({
    "success": True,
    "routes": routes
  })