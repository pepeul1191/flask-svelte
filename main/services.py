# main/services.py
class ApplicationService:

  @staticmethod
  def build_response(data=None, message=None, error=None, success=True):
    return {
      "data": data,
      "message": message,
      "error": error,
      "success": success
    }

  @staticmethod
  def handle_error(message, error_details=None):
    return ApplicationService.build_response(
      data=None,
      message=message,
      error=error_details or message,
      success=False
    )

  @staticmethod
  def handle_not_found(message="Registro no encontrado"):
    return ApplicationService.handle_error(
      message,
      "Registro no encontrado en el sistema"
    )

  @staticmethod
  def handle_validation_error(errors):
    """
    errors puede ser:
    - dict (Marshmallow / Pydantic style)
    - list de strings
    """
    if isinstance(errors, dict):
      error_message = ", ".join([
        f"{k}: {', '.join(v)}" if isinstance(v, list) else f"{k}: {v}"
        for k, v in errors.items()
      ])
    elif isinstance(errors, list):
      error_message = ", ".join(errors)
    else:
      error_message = str(errors)

    return ApplicationService.handle_error(
      f"Error de validación: {error_message}",
      error_message
    )