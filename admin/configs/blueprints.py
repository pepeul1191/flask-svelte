# admin/configs/blueprints.py
# views
from admin.views.index import views as index_views
from admin.views.oil_brand_view import views as oil_brand_view
from admin.views.oil_type_view import views as oil_type_view
from admin.views.oil_view import views as oil_view
from admin.views.brand_view import views as brand_view
# apis

blueprints = [
  # views
  index_views,
  oil_brand_view,
  oil_type_view,
  oil_view,
  brand_view,
  # apis
]