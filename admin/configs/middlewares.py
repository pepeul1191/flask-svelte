# admin/configs/middlewares.py
from functools import wraps
from flask import session, redirect, jsonify, request

def only_logged(fn):
  @wraps(fn)
  def _only_logged(*args, **kwargs):
    roles = session.get("roles", [])

    if "admin" not in roles:
      # Si la ruta comienza con /api -> responder JSON
      if request.path.startswith("/api"):
        return jsonify({
          "data": None,
          "message": "No autorizado",
          "error": True,
          "success": False
        }), 403

      # Si no es API -> mostrar la página de error
      return redirect("/error/403")
      # o:
      # return render_template("errors/404.html"), 404

    return fn(*args, **kwargs)

  return _only_logged