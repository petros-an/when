from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler

class ErrorDisplayValidationError(ValidationError):
    def __init__(self, detail=None, code=None):
        super().__init__(detail, code)
        if isinstance(detail, str):
            self.display_message = detail
        elif isinstance(detail, list):
            self.display_message = ', '.join(detail)
        elif isinstance(detail, dict):
            self.display_message = ', '.join(detail.items())


def error_display_exception_handler(exc, context):
    response = exception_handler(exc, context)
    detail = exc.detail
    if isinstance(detail, str):
        response.data['display_message'] = detail
    elif isinstance(detail, list):
        response.data['display_message'] = ', '.join(detail)
    elif isinstance(detail, dict):
        response.data['display_message'] = ', '.join(list(detail.values())[0])
    return response
