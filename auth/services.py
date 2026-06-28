# auth/services.py
import os
import requests
from main.services import ApplicationService

class AuthService(ApplicationService):

  @staticmethod
  def simple_login(username: str, password: str):

    admin_username = os.getenv("USERNAME")
    admin_password = os.getenv("PASSWORD")

    if not admin_username or not admin_password:
      return AuthService.handle_error("admin credentials not configured")

    if username == admin_username and password == admin_password:

      login_response = {
        "user": {
          "id": 1,
          "username": admin_username,
          "name": "Admin User",
          "email": "jovaldiv@ulima.edu.pe"
        },
        "roles": ["admin"],
        "tokens": {
          "access": os.getenv("ACCESS_TOKEN"),
          "file": os.getenv("FILES_TOKEN")
        }
      }

      return AuthService.build_response(
        data=login_response,
        message="Admin login successful"
      )

    return AuthService.handle_error("Invalid credentials")

  @staticmethod
  def login_by_username(username: str, password: str):

    if not username or not password:
      return AuthService.handle_error(
        "username and password are required"
      )

    access_api = AuthService._make_auth_access_request(username, password)
    if not access_api["success"]:
      return access_api

    files_api = AuthService._make_auth_files_request()
    if not files_api["success"]:
      return files_api

    access_data = access_api["data"]
    files_data = files_api["data"]

    login_response = {
      "user": access_data["data"]["user"],
      "roles": access_data["data"]["roles"],
      "tokens": {
        "access": access_data["data"]["token"],
        "file": files_data["data"]["token"]
      }
    }

    return AuthService.build_response(
      data=login_response,
      message="Login successful"
    )

  @staticmethod
  def google_token_valid(token: str):
    if not token:
      return False

    try:
      resp = requests.get(
        f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={token}",
        timeout=10
      )
      return resp.status_code == 200
    except:
      return False

  @staticmethod
  def refresh_google_token(user):

    refresh_token = getattr(user, "google_refresh_token", None)

    if not refresh_token:
      return AuthService.handle_error("User has no refresh token")

    try:
      resp = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
          "client_id": os.getenv("GOOGLE_CLIENT_ID"),
          "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
          "refresh_token": refresh_token,
          "grant_type": "refresh_token"
        },
        headers={
          "Content-Type": "application/x-www-form-urlencoded"
        },
        timeout=10
      )

      if resp.status_code == 200:
        data = resp.json()

        if hasattr(user, "google_token"):
          user.google_token = data.get("access_token")

        return AuthService.build_response(
          data={"token": data.get("access_token")},
          message="Token refreshed successfully"
        )

      return AuthService.handle_error(
        f"Failed to refresh token: {resp.status_code}"
      )

    except Exception as e:
      return AuthService.handle_error(
        "Error refreshing token",
        str(e)
      )

  # =====================================================
  # PRIVATE METHODS
  # =====================================================

  @staticmethod
  def _make_auth_files_request():

    url = os.getenv("URL_FILES_SERVICE")
    x_auth = os.getenv("X_AUTH_FILES_SERVICE")

    if not url or not x_auth:
      return AuthService.handle_error(
        "files service is not available (missing configuration)"
      )

    try:
      resp = requests.post(
        f"{url}/api/v1/sign-in",
        json={},
        headers={
          "X-Auth-Trigger": x_auth
        },
        timeout=30
      )

      if resp.status_code < 400:
        return AuthService.build_response(
          data=resp.json(),
          message="Files authentication successful"
        )

      return AuthService.handle_error(
        resp.json().get("message", "Error in files service"),
        resp.text
      )

    except Exception as e:
      return AuthService.handle_error(
        "could not connect to the files service",
        str(e)
      )

  @staticmethod
  def _make_auth_access_request(username: str, password: str):

    url = os.getenv("URL_ACCESS_SERVICE")
    x_auth = os.getenv("X_AUTH_ACCESS_SERVICE")
    system_id = os.getenv("SYSTEM_ID")

    if not url or not x_auth or not system_id:
      return AuthService.handle_error(
        "authentication service is not available (missing configuration)"
      )

    try:
      payload = {
        "username": username,
        "password": password,
        "system_id": int(system_id)
      }

      resp = requests.post(
        f"{url}/api/v1/users/sign-in/by-username",
        json=payload,
        headers={
          "X-Auth-Trigger": x_auth
        },
        timeout=30
      )

      if resp.status_code < 400:
        return AuthService.build_response(
          data=resp.json(),
          message="Authentication successful"
        )

      return AuthService.handle_error(
        resp.json().get("message", "Error in authentication service"),
        resp.text
      )

    except Exception as e:
      return AuthService.handle_error(
        "could not connect to the authentication service",
        str(e)
      )

  @staticmethod
  def health_check():

    url = os.getenv("URL_ACCESS_SERVICE")

    if not url:
      return AuthService.handle_error(
        "Authentication service URL not configured"
      )

    try:
      resp = requests.get(f"{url}/health", timeout=5)

      if resp.status_code < 400:
        return AuthService.build_response(
          message="Authentication service available"
        )

      return AuthService.handle_error(
        "Authentication service not available"
      )

    except Exception as e:
      return AuthService.handle_error(str(e))