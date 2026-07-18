from flask import Blueprint, flash, render_template, request, redirect

from admin.configs.middlewares import only_logged
from admin.services.level_service import LevelService
from admin.services.courses_service import CourseService
from admin.services.section_service import SectionService
from admin.services.advert_service import AdvertService


views = Blueprint(
  "admin-adverts-views",
  __name__,
  template_folder="../templates"
)


# =====================
# INDEX
# =====================
@views.route("/admin/levels/<int:level_id>/courses/<int:course_id>/sections/<int:section_id>/adverts", methods=["GET"])
@only_logged
def index(level_id, course_id, section_id):

  level_response = LevelService.fetch_one(level_id)

  if not level_response["success"]:
    flash(level_response["message"], "danger")
    return redirect("/admin/levels")


  course_response = CourseService.fetch_one(
    level_id,
    course_id
  )

  if not course_response["success"]:
    flash(course_response["message"], "danger")
    return redirect(f"/admin/levels/{level_id}/courses")


  section_response = SectionService.fetch_one(
    course_id,
    section_id
  )

  if not section_response["success"]:
    flash(section_response["message"], "danger")
    return redirect(f"/admin/levels/{level_id}/courses/{course_id}/sections")


  page = request.args.get("page", 1, type=int)
  per_page = request.args.get("per_page", 10, type=int)

  published_from_start = request.args.get(
    "published_from_start",
    ""
  )

  published_from_end = request.args.get(
    "published_from_end",
    ""
  )


  if page < 1:
    page = 1

  if per_page < 1:
    per_page = 10


  response = AdvertService.fetch_all(
    page=page,
    per_page=per_page,
    section_id=section_id,
    published_from_start=published_from_start or None,
    published_from_end=published_from_end or None
  )


  adverts = []

  pagination = {
    "page": page,
    "per_page": per_page,
    "total_adverts": 0,
    "total_pages": 0,
    "start_record": 0,
    "end_record": 0
  }


  if response["success"]:
    adverts = response["data"]["adverts"]
    pagination = response["data"]["pagination"]
  else:
    flash(response["message"], "danger")


  return render_template(
    "sections/adverts.html",
    locals={
      "title": "Anuncios",
      "nav_link": "academic-management",
      "level_id": level_id,
      "course_id": course_id,
      "section_id": section_id,
      "level": level_response["data"],
      "course": course_response["data"],
      "section": section_response["data"],
      "adverts": adverts,
      "pagination": pagination,
      "published_from_start": published_from_start,
      "published_from_end": published_from_end
    }
  )

# =====================
# UPDATE
# =====================
@views.route("/admin/levels/<int:level_id>/courses/<int:course_id>/sections/<int:section_id>/adverts/<int:advert_id>/update", methods=["POST"])
@only_logged
def update(level_id, course_id, section_id, advert_id):

  response = AdvertService.update(
    advert_id,
    {
      "visible": request.form.get("visible") == "1"
    }
  )

  if response["success"]:
    flash(response["message"], "success")
  else:
    flash(response["message"], "danger")


  page = request.form.get(
    "page",
    1
  )

  per_page = request.form.get(
    "per_page",
    10
  )

  published_from_start = request.form.get(
    "published_from_start",
    ""
  )

  published_from_end = request.form.get(
    "published_from_end",
    ""
  )


  return redirect(
    f"/admin/levels/{level_id}/courses/{course_id}/sections/{section_id}/adverts"
    f"?page={page}"
    f"&per_page={per_page}"
    f"&published_from_start={published_from_start}"
    f"&published_from_end={published_from_end}"
  )

# =====================
# DELETE
# =====================
@views.route("/admin/levels/<int:level_id>/courses/<int:course_id>/sections/<int:section_id>/adverts/<int:advert_id>/delete", methods=["GET"])
@only_logged
def delete(level_id, course_id, section_id, advert_id):

  response = AdvertService.delete(advert_id)

  if response["success"]:
    flash(response["message"], "success")
  else:
    flash(response["message"], "danger")

  return redirect(
    f"/admin/levels/{level_id}/courses/{course_id}/sections/{section_id}/adverts"
  )