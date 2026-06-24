# admin/configs/blueprints.py
from admin.views.index import views as index_views
from admin.views.locations import views as locations_views
from admin.views.respresentative_role import views as respresentative_role_views

blueprints = [
  index_views,
  locations_views,
  respresentative_role_views,
]