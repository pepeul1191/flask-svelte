# admin/configs/blueprints.py
from admin.views.index import views as index_views
from admin.views.locations import views as locations_views

blueprints = [
  index_views,
  locations_views,
]