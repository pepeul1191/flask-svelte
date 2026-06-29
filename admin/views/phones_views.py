# admin/views/phones_views.py

from flask import Blueprint, flash, redirect, request, render_template

from admin.configs.middlewares import only_logged
from admin.services.phone_service import PhoneService
from admin.services.worker_service import WorkerService

views = Blueprint('admin-phone-views', __name__, template_folder='../templates')

@views.route("/admin/phones/new", methods=["GET"])
@only_logged
def phone_new():
  worker_id = request.args.get('worker_id')

  response = WorkerService.fetch_one(worker_id)

  if not response["success"]:
    flash(response["message"], "danger")
    return redirect("/admin/workers")
  
  return render_template(
    "phone/new.html",
    locals={
      "title": "Agregar Teléfono a Trabajador",
      "nav_link": "worker-management",
      "worker_id": worker_id,
      "person": response["data"]["person"],
    }
  )

@views.route("/admin/phones", methods=["POST"])
@only_logged
def phone_create():
  worker_id = request.form.get('worker_id')
  response = PhoneService.create(request.form)

  if response["success"]:
    # En caso de que la persona se actualice pero no se encuentre su Worker
    flash("Se ha agregado teléfono a trabajador", "success")
    return redirect(f"/admin/workers/{worker_id}/edit")

  flash(response["message"], "danger")
  return redirect(request.referrer)

@views.route('/admin/phones/<int:phone_id>/edit', methods=["GET"])
@only_logged
def edit_phone(phone_id):
  """Muestra el formulario para editar un teléfono"""
  worker_id = request.args.get('worker_id')

  response = WorkerService.fetch_one(worker_id)

  if not response["success"]:
    flash(response["message"], "danger")
    return redirect("/admin/workers")

  # Obtener datos del teléfono
  phone_result = PhoneService.fetch_one(phone_id)

  if not phone_result.get('success'):
    flash('Teléfono no encontrado', 'danger')
    return redirect(f'/admin/workers/{worker_id}/edit' if worker_id else '/admin/workers')
  
  locals = {
    "phone": phone_result.get('data'),
    "worker": response['data']
  }

  return render_template(
    'phones/edit.html',
    locals=locals
  )


@views.route('/admin/phones/<int:phone_id>/edit', methods=["POST"])
@only_logged
def update_phone(phone_id):
  """Actualiza un teléfono"""
  params = {
    'person_id': request.form.get('person_id'),
    'description': request.form.get('description'),
    'phone': request.form.get('phone')
  }
  worker_id = request.form.get('worker_id')

  result = PhoneService.update(phone_id, params)

  if result.get('success'):
    flash('Teléfono actualizado exitosamente', 'success')
    if worker_id:
      return redirect(f'/admin/workers/{worker_id}/edit')
    return redirect('/admin/workers')
  else:
    flash(f'Error al actualizar teléfono: {result.get("error", "Error desconocido")}', 'danger')
    # Volver al formulario con los datos
    phone_result = PhoneService.fetch_one(phone_id)
    person_result = PersonService.fetch_one(params.get('person_id'))
    return render_template(
      'phones/edit.html',
      phone=phone_result.get('data'),
      person=person_result.get('data'),
      worker_id=worker_id
    )


@views.route('/admin/phones/<int:phone_id>/delete', methods=["GET"])
@only_logged
def delete_phone(phone_id):
  """Elimina un teléfono y redirige a la vista de edición del trabajador"""

  # Obtener worker_id de los parámetros
  worker_id = request.args.get('worker_id')

  if not worker_id:
    flash('No se pudo identificar el trabajador', 'warning')
    return redirect('/admin/workers')

  # Eliminar el teléfono
  result = PhoneService.delete(phone_id)

  if result.get('success'):
    flash('Teléfono eliminado exitosamente', 'success')
  else:
    flash(f'Error al eliminar teléfono: {result.get("error", "Error desconocido")}', 'danger')

  # Redirigir a la edición del trabajador
  return redirect(f'/admin/workers/{worker_id}/edit')
  