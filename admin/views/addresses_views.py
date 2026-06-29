# admin/views/addresses_viewss.py

from flask import Blueprint, flash, redirect, request, render_template

from admin.configs.middlewares import only_logged
from admin.services.address_service import AddressService
from admin.services.worker_service import WorkerService

views = Blueprint('admin-address-views', __name__, template_folder='../templates')

@views.route("/admin/addresses/new", methods=["GET"])
@only_logged
def address_new():
  worker_id = request.args.get('worker_id')

  response = WorkerService.fetch_one(worker_id)

  if not response["success"]:
    flash(response["message"], "danger")
    return redirect("/admin/workers")

  return render_template(
    "addresses/new.html",
    locals={
      "title": "Agregar Dirección a Trabajador",
      "nav_link": "worker-management",
      "worker_id": worker_id,
      "person": response["data"]["person"],
    }
  )

@views.route("/admin/addresses", methods=["POST"])
@only_logged
def address_create():
  worker_id = request.form.get('worker_id')
  response = AddressService.create(request.form)

  if response["success"]:
    flash("Se ha agregado dirección al trabajador", "success")
    return redirect(f"/admin/workers/{worker_id}/edit")

  flash(response["message"], "danger")
  return redirect(request.referrer)

@views.route('/admin/addresses/<int:address_id>/edit', methods=["GET"])
@only_logged
def edit_address(address_id):
  """Muestra el formulario para editar una dirección"""
  worker_id = request.args.get('worker_id')

  response = WorkerService.fetch_one(worker_id)

  if not response["success"]:
    flash(response["message"], "danger")
    return redirect("/admin/workers")

  # Obtener datos de la dirección
  address_result = AddressService.fetch_one(address_id)

  if not address_result.get('success'):
    flash('Dirección no encontrada', 'danger')
    return redirect(f'/admin/workers/{worker_id}/edit' if worker_id else '/admin/workers')

  locals_data = {
    "address": address_result.get('data'),
    "worker": response['data']
  }

  return render_template(
    'addresses/edit.html',
    locals=locals_data
  )

@views.route('/admin/addresses/<int:address_id>/edit', methods=["POST"])
@only_logged
def update_address(address_id):
  """Actualiza una dirección"""
  params = {
    'person_id': request.form.get('person_id'),
    'district_id': request.form.get('district_id'),
    'description': request.form.get('description'),
    'address': request.form.get('address')
  }
  worker_id = request.form.get('worker_id')

  result = AddressService.update(address_id, params)

  if result.get('success'):
    flash('Dirección actualizada exitosamente', 'success')
    if worker_id:
      return redirect(f'/admin/workers/{worker_id}/edit')
    return redirect('/admin/workers')
  else:
    flash(f'Error al actualizar dirección: {result.get("error", "Error desconocido")}', 'danger')
    # Volver al formulario con los datos
    address_result = AddressService.fetch_one(address_id)
    return render_template(
      'addresses/edit.html',
      address=address_result.get('data'),
      worker_id=worker_id
    )

@views.route('/admin/addresses/<int:address_id>/delete', methods=["GET"])
@only_logged
def delete_address(address_id):
  """Elimina una dirección y redirige a la vista de edición del trabajador"""

  # Obtener worker_id de los parámetros
  worker_id = request.args.get('worker_id')

  if not worker_id:
    flash('No se pudo identificar el trabajador', 'warning')
    return redirect('/admin/workers')

  # Eliminar la dirección
  result = AddressService.delete(address_id)

  if result.get('success'):
    flash('Dirección eliminada exitosamente', 'success')
  else:
    flash(f'Error al eliminar dirección: {result.get("error", "Error desconocido")}', 'danger')

  # Redirigir a la edición del trabajador
  return redirect(f'/admin/workers/{worker_id}/edit')