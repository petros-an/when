from django.db.models import Prefetch, Count
from rest_framework import viewsets

from app.models import Event, When
from app.serializers.events import EventRetrieveSerializer, EventCreateSerializer, EventUpdateSerializer


class EventViewset(viewsets.ModelViewSet):

    def get_queryset(self):
        qs = Event.objects.filter(status='accepted').prefetch_related(
            Prefetch(
                'whens',
                queryset=When.objects.filter(status='accepted')
            )
        ).annotate(
            vote_count=Count('votes')
        )
        category = self.kwargs.get('category')
        if category:
            qs = qs.filter(category=category)
        return qs

    def get_serializer(self, *args, **kwargs):
        context = self.get_serializer_context()
        if self.action == 'list' or self.action == 'retrieve':
            return EventRetrieveSerializer(*args, **kwargs, context=context)
        elif self.action == 'create':
            return EventCreateSerializer(*args, **kwargs, context=context)
        elif self.action == 'update' or self.action == 'partial_update':
            return EventUpdateSerializer(*args, **kwargs, context=context)

    def perform_destroy(self, instance):
        instance.status = 'deleted'
        instance.save()