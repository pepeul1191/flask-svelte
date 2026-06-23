# auth/views.py
from flask import Blueprint, flash, redirect, render_template, request, session

from auth.services import AuthService

views = Blueprint('auth-views', __name__, template_folder='./templates')

@views.route('/sign-in', methods=['GET', 'POST'])
def login():
  if request.method == 'GET':
    locals = {
      'title': 'Home',
      'nav_active': 'home',
      'message': '',
    }
    return render_template('./sign-in.html', locals=locals)

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
    # en función al rol el redirect
    roles = user_data.get("roles", [])

    if "admin" in roles:
      return redirect("/admin")

    return redirect('/')

  # =========================
  # ERROR (flash Rails equivalent)
  # =========================
  flash(result.get("message"), "danger")

  return render_template('./sign-in.html')

@views.route('/reset-password', methods=["GET"])
def reset_password():
  return render_template('./reset-password.html')

@views.route('/sign-up', methods=["GET"])
def sign_up():
  return render_template('./sign-up.html')

@views.route('/sign-out', methods=["GET"])
def sign_out():
  session.clear()
  flash("Gracias, vuelva pronto", "success")
  return redirect('/sign-in')