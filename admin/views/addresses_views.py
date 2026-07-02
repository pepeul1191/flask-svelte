# admin/views/addresses_views.py

from flask import Blueprint, flash, redirect, request, render_template

from admin.configs.middlewares import only_logged
from admin.services.address_service import AddressService
from admin.services.worker_service import WorkerService
from admin.services.representative_service import RepresentativeService
# from admin.services.student_service import StudentService  # Comentado: clase aún no disponible

views = Blueprint('admin-address-views', __name__, template_folder='../templates')

# Mapeo de tipos de entidad a sus servicios
ENTITY_SERVICES = {
  'worker': WorkerService,
  'representative': RepresentativeService,
  # 'student': StudentService,  # Comentado: clase aún no disponible
}

# Mapeo de tipos de entidad a sus rutas de redirección
ENTITY_REDIRECTS = {
  'worker': '/admin/workers',
  'representative': '/admin/representatives',
  # 'student': '/admin/students',  # Comentado: ruta aún no disponible
}

# Mapeo de tipos de entidad a sus nombres para mostrar
ENTITY_NAMES = {
  'worker': 'Trabajador',
  'representative': 'Apoderado',
  # 'student': 'Estudiante',  # Comentado: entidad aún no disponible
}


def get_entity_service(entity_type):
  """Obtiene el servicio correspondiente al tipo de entidad"""
  service = ENTITY_SERVICES.get(entity_type)
  if not service:
    return None
  return service


def get_entity_redirect(entity_type):
  """Obtiene la ruta de redirección para el tipo de entidad"""
  return ENTITY_REDIRECTS.get(entity_type, '/admin/dashboard')


def get_entity_name(entity_type):
  """Obtiene el nombre legible del tipo de entidad"""
  return ENTITY_NAMES.get(entity_type, 'Entidad')


@views.route("/admin/addresses/new", methods=["GET"])
@only_logged
def address_new():
  entity_type = request.args.get('entity_type', 'worker')
  entity_id = request.args.get('worker_id') or request.args.get('representative_id') or request.args.get('student_id')
  
  if not entity_id:
    flash("ID de entidad no proporcionado", "danger")
    return redirect(get_entity_redirect(entity_type))
  
  service = get_entity_service(entity_type)
  if not service:
    flash("Tipo de entidad no válido", "danger")
    return redirect('/admin/dashboard')
  
  response = service.fetch_one(entity_id)

  if not response["success"]:
    flash(response["message"], "danger")
    return redirect(get_entity_redirect(entity_type))
  
  entity_name = get_entity_name(entity_type)
  
  return render_template(
    "addresses/new.html",
    locals={
      "title": f"Agregar Dirección a {entity_name}",
      "nav_link": f"{entity_type}-management",
      "entity_type": entity_type,
      "entity_id": entity_id,
      "person": response["data"]["person"],
    }
  )


@views.route("/admin/addresses", methods=["POST"])
@only_logged
def address_create():
  entity_type = request.form.get('entity_type', 'worker')
  entity_id = request.form.get('worker_id') or request.form.get('representative_id') or request.form.get('student_id')
  
  if not entity_id:
    flash("ID de entidad no proporcionado", "danger")
    return redirect(get_entity_redirect(entity_type))
  
  response = AddressService.create(request.form)

  if response["success"]:
    flash("Se ha agregado dirección", "success")
    return redirect(f"/admin/{entity_type}s/{entity_id}/edit")

  flash(response["message"], "danger")
  return redirect(request.referrer)


@views.route('/admin/addresses/<int:address_id>/edit', methods=["GET"])
@only_logged
def edit_address(address_id):
  """Muestra el formulario para editar una dirección"""
  entity_type = request.args.get('entity_type', 'worker')
  entity_id = request.args.get('worker_id') or request.args.get('representative_id') or request.args.get('student_id')
  
  if not entity_id:
    flash("ID de entidad no proporcionado", "danger")
    return redirect(get_entity_redirect(entity_type))
  
  service = get_entity_service(entity_type)
  if not service:
    flash("Tipo de entidad no válido", "danger")
    return redirect('/admin/dashboard')

  response = service.fetch_one(entity_id)

  if not response["success"]:
    flash(response["message"], "danger")
    return redirect(get_entity_redirect(entity_type))

  # Obtener datos de la dirección
  address_result = AddressService.fetch_one(address_id)

  if not address_result.get('success'):
    flash('Dirección no encontrada', 'danger')
    return redirect(f'/admin/{entity_type}s/{entity_id}/edit')

  locals_data = {
    "address": address_result.get('data'),
    "entity": response['data'],
    "entity_type": entity_type,
    "entity_id": entity_id,
  }

  return render_template(
    'addresses/edit.html',
    locals=locals_data
  )


@views.route('/admin/addresses/<int:address_id>/edit', methods=["POST"])
@only_logged
def update_address(address_id):
  """Actualiza una dirección"""
  entity_type = request.form.get('entity_type', 'worker')
  entity_id = request.form.get('worker_id') or request.form.get('representative_id') or request.form.get('student_id')
  
  if not entity_id:
    flash("ID de entidad no proporcionado", "danger")
    return redirect(get_entity_redirect(entity_type))
  
  params = {
    'entity_type': entity_type,
    f'{entity_type}_id': entity_id,
    'district_id': request.form.get('district_id'),
    'description': request.form.get('description'),
    'address': request.form.get('address')
  }

  result = AddressService.update(address_id, params)

  if result.get('success'):
    flash('Dirección actualizada exitosamente', 'success')
    return redirect(f'/admin/{entity_type}s/{entity_id}/edit')
  else:
    flash(f'Error al actualizar dirección: {result.get("error", "Error desconocido")}', 'danger')
    # Volver al formulario con los datos
    address_result = AddressService.fetch_one(address_id)
    service = get_entity_service(entity_type)
    if service:
      entity_result = service.fetch_one(entity_id)
      entity_data = entity_result.get('data') if entity_result.get('success') else None
    else:
      entity_data = None
      
    return render_template(
      'addresses/edit.html',
      locals={
        'address': address_result.get('data'),
        'entity': entity_data,
        'entity_type': entity_type,
        'entity_id': entity_id,
      }
    )


@views.route('/admin/addresses/<int:address_id>/delete', methods=["GET"])
@only_logged
def delete_address(address_id):
  """Elimina una dirección y redirige a la vista de edición de la entidad correspondiente"""
  entity_type = request.args.get('entity_type', 'worker')
  entity_id = request.args.get('worker_id') or request.args.get('representative_id') or request.args.get('student_id')

  if not entity_id:
    flash('No se pudo identificar la entidad', 'warning')
    return redirect(get_entity_redirect(entity_type))

  # Eliminar la dirección
  result = AddressService.delete(address_id)

  if result.get('success'):
    flash('Dirección eliminada exitosamente', 'success')
  else:
    flash(f'Error al eliminar dirección: {result.get("error", "Error desconocido")}', 'danger')

  # Redirigir a la edición de la entidad
  return redirect(f'/admin/{entity_type}s/{entity_id}/edit')