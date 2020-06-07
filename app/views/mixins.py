from django.views import View
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ViewSet


class AllowAnyForRead(object):
    def get_permissions(self):
        if isinstance(self, ViewSet):
            if self.action in ['list', 'retrieve']:
                self.permission_classes = (AllowAny,)

        elif isinstance(self, View):
            if self.request.method in ['GET']:
                self.permission_classes = (AllowAny,)

        return super().get_permissions()