# main/blueprints.py
# from admin.blueprints import blueprints as admin_blueprints
from web.blueprints import blueprints as web_blueprints
from auth.blueprints import blueprints as auth_blueprints

def register(app):
  # append sub blueprints
  modules_blueprints = [
    # admin_blueprints,
    web_blueprints,
    auth_blueprints
  ]
  # load sub blueprints to app
  for blueprints in modules_blueprints:
    for blueprint in blueprints:
      app.register_blueprint(blueprint)

