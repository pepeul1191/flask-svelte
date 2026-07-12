# admin/configs/blueprints.py
# views
from admin.views.index import views as index_views
from admin.views.locations_views import views as locations_views
from admin.views.respresentative_role_views import views as respresentative_role_views
from admin.views.level_views import views as level_views
from admin.views.workers_views import views as worker_views
from admin.views.phones_views import views as phone_views
from admin.views.addresses_views import views as addresses_views
from admin.views.representatives_views import views as representatives_views
from admin.views.students_views import views as students_views
from admin.views.courses_views import views as courses_views
# apis
from admin.apis.districts_apis import apis as district_apis
from admin.apis.representative_student_role_apis import apis as representative_student_role_apis
from admin.apis.representatives_apis import apis as representatives_apis
from admin.apis.students_apis import apis as students_apis
from admin.apis.workers_apis import apis as worker_apis

blueprints = [
  # views
  index_views,
  locations_views,
  respresentative_role_views,
  level_views,
  worker_views,
  phone_views,
  addresses_views,
  representatives_views,
  students_views,
  courses_views,
  # apis
  district_apis,
  representative_student_role_apis,
  representatives_apis,
  students_apis, 
  worker_apis,
]