from rest_framework import viewsets
from app.models import When
from app.serializers.whens import WhenRetrieveSerializer, WhenCreateSerializer, WhenUpdateSerializer


class EventWhenViewset(viewsets.ModelViewSet):

    serializer_class = WhenRetrieveSerializer

    def get_queryset(self):
        return When.objects.filter(event_id=self.kwargs["event_pk"])

    def get_serializer(self, *args, **kwargs):
        context = self.get_serializer_context()
        if self.action == 'list' or self.action == 'retrieve':
            return WhenRetrieveSerializer(*args, **kwargs, context=context)
        elif self.action == 'create':
            return WhenCreateSerializer(*args, **kwargs, context=context)
        elif self.action == 'update' or self.action == 'partial_update':
            return WhenUpdateSerializer(*args, **kwargs, context=context)

