from django.views import View
from rest_framework.exceptions import ValidationError, APIException
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ViewSet

from app.exceptions import ErrorDisplayValidationError


class AllowAnyForRead(object):
    def get_permissions(self):
        if isinstance(self, ViewSet):
            if self.action in ['list', 'retrieve']:
                self.permission_classes = (AllowAny,)

        elif isinstance(self, View):
            if self.request.method in ['GET']:
                self.permission_classes = (AllowAny,)

        return super().get_permissions()


class DisplayErrorMixin(object):
    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        detail = exc.detail
        if isinstance(detail, str):
            display_message = detail
        elif isinstance(detail, list):
            display_message = ', '.join(detail)
        elif isinstance(detail, dict):
            display_message = ', '.join(list(detail.values())[0])
        response.data['display_message'] = display_message
        return response


