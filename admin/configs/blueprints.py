# admin/configs/blueprints.py
# views
from admin.views.index import views as index_views
from admin.views.oil_brand_view import views as oil_brand_view
from admin.views.oil_type_view import views as oil_type_view
from admin.views.oil_view import views as oil_view
from admin.views.brand_view import views as brand_view
from admin.views.brand_model_view import views as brand_model_view
from admin.views.worker_view import views as worker_view
from admin.views.client_view import views as client_view
from admin.views.client_worker_view import views as client_worker_view
from admin.views.machine_view import views as machine_view
# apis

blueprints = [
  # views
  index_views,
  oil_brand_view,
  oil_type_view,
  oil_view,
  brand_view,
  brand_model_view,
  worker_view,
  client_view,
  client_worker_view,
  machine_view,
  # apis
]