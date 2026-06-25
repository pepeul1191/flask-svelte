# main/middlewares.py
from functools import wraps
from flask import session, redirect, request, Response, jsonify, render_template

def only_logged(fn):
  @wraps(fn)
  def _only_logged(*args, **kwargs):
    # si la session es activaa, vamos a '/accesos/'
    if session.get('status'):
      if session.get('status') == False:
        return redirect('/error/403')
    else:
      return redirect('/error/403')
    return fn(*args, **kwargs)
  return _only_logged

def logged_go_admin(fn):
  @wraps(fn)
  def _logged_go_admin(*args, **kwargs):
    # si la session es activaa, vamos a '/accesos/'
    if session.get('status'):
      if session.get('status') == True:
        return redirect('/admin')
      else:
        fn(*args, **kwargs)
    else:
      fn(*args, **kwargs)
    return fn(*args, **kwargs)
  return _logged_go_admin

def not_found(e):
  path = request.path

  static_extensions = ('.css', '.js', '.woff', '.png', '.jpg', '.jpeg', '.svg', '.ico')

  # 1. ARCHIVOS ESTÁTICOS → cortar respuesta silenciosa
  if path.endswith(static_extensions):
    return Response(status=404)  # no body, request "muere" aquí

  # 2. API → JSON genérico
  if path.startswith('/api/'):
    return jsonify({
      "data": None,
      "message": "Recurso no encontrado",
      "error": True,
      "success": False
    }), 404

  # 3. FRONTEND → redirect
  #return redirect('/error/404')
  # template es web/templates/404.html
  return render_template('404.html'), 404

def set_global_headers(response):
  response.headers["Server"] = "Werkzeug/3.1.8 Python/3.12.3/Ubuntu"
  return response