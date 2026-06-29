# admin/configs/blueprints.py
from admin.views.index import views as index_views
from admin.views.locations_views import views as locations_views
from admin.views.respresentative_role import views as respresentative_role_views
from admin.views.level import views as level_views
from admin.views.workers_views import views as worker_views
from admin.views.phones_views import views as phone_views
from admin.apis.district_apis import apis as district_apis

blueprints = [
  index_views,
  locations_views,
  respresentative_role_views,
  level_views,
  worker_views,
  phone_views,
  district_apis,
]