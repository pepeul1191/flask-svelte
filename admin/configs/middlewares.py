# admin/configs/middlewares.py
from functools import wraps
from flask import session, redirect

def only_logged(fn):
  @wraps(fn)
  def _only_logged(*args, **kwargs):

    roles = session.get("roles", [])

    if "admin" not in roles:
      return redirect("/error/403")

    return fn(*args, **kwargs)

  return _only_logged