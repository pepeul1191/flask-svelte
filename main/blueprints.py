# main/blueprints.py
# from admin.blueprints import blueprints as admin_blueprints
from main.application import csrf
# modules blueprints
from web.blueprints import blueprints as web_blueprints
from auth.blueprints import blueprints as auth_blueprints
from admin.configs.blueprints import blueprints as admin_blueprints
# doules apis for csrf excluding
from auth.apis import apis as auth_apis

def register(app):
  # append sub blueprints
  modules_blueprints = [
    # admin_blueprints,
    web_blueprints,
    auth_blueprints,
    admin_blueprints,
  ]
  # load sub blueprints to app
  for blueprints in modules_blueprints:
    for blueprint in blueprints:
      app.register_blueprint(blueprint)
  # Excluir blueprint API del CSRF
  csrf.exempt(auth_apis)