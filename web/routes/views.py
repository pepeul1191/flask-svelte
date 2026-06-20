# web/configs/views.py
from flask import Blueprint, flash, redirect, render_template, request, session

from web.services.auth_service import AuthService

view = Blueprint('web-view', __name__)

@view.route('/', methods=['GET'])
def index():
  locals = {
    'title': 'Home',
    'nav_active': 'home',
    'message': '',
  }
  return render_template('web/index.html', locals=locals)

@view.route('/incubadora', methods=['GET'])
def incubadora():
  locals = {
    'title': 'Inncuvadora',
    'nav_active': 'home',
    'message': '',
  }
  return render_template('web/incubadora.html', locals=locals)

@view.route('/sign-in', methods=['GET', 'POST'])
def login():

  if request.method == 'GET':
    return render_template('web/sign_in.html')

  username = request.form.get('username')
  password = request.form.get('password')

  # result = AuthService.login_by_username(username, password)
  result = AuthService.simple_login(username, password)

  print(result)

  if result.get("success"):

    user_data = result["data"]

    # =========================
    # SESSION (equivalente Rails)
    # =========================

    session['user'] = {
      "id": user_data["user"]["id"],
      "username": user_data["user"]["username"],
      "name": user_data["user"].get("name", user_data["user"]["username"]),
      "email": user_data["user"]["email"],
      "oauth": False
    }

    session['tokens'] = user_data.get("tokens", {})
    session['roles'] = user_data.get("roles", [])

    """
    # =========================
    # LOGIN LOG (equivalente Rails model)
    # =========================
    try:
      from main.models.login_log import LoginLog

      log = LoginLog(
        user_id=user_data["user"]["id"],
        success=True,
        ip_address=request.remote_addr,
        created_at=datetime.utcnow()
      )
      log.save()

    except Exception as e:
      print("LoginLog error:", e)
    """

    return redirect('/')

  # =========================
  # ERROR (flash Rails equivalent)
  # =========================
  flash(result.get("message", "Login failed"), "danger")

  return render_template('web/sign_in.html')

@view.route('/error/403')
def error_403():
  return render_template('web/403.html')

@view.route('/error/404')
def error_404():
  return render_template('web/404.html'), 404