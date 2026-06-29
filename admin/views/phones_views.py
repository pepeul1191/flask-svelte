# admin/views/phones_views.py

from flask import Blueprint, flash, redirect, request

from admin.configs.middlewares import only_logged
from admin.services.phone_service import PhoneService

views = Blueprint('admin-phone-views', __name__, template_folder='../templates')


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