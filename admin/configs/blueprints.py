# admin/configs/blueprints.py
from admin.views.index import views as index_views
from admin.views.locations import views as locations_views
from admin.views.respresentative_role import views as respresentative_role_views
from admin.views.level import views as level_views
from admin.views.worker import views as worker_views

blueprints = [
  index_views,
  locations_views,
  respresentative_role_views,
  level_views,
  worker_views,
]