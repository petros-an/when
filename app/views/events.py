from django.contrib.postgres.search import SearchVector
from django.db.models import Prefetch, Count
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView

from app.models import Event, When
from app.serializers.events import EventRetrieveSerializer, EventCreateSerializer, EventUpdateSerializer, \
    EventAutocompleteSerializer


class EventViewset(viewsets.ModelViewSet):

    def get_queryset(self):
        qs = Event.objects.filter(status='accepted').prefetch_related(
            Prefetch(
                'whens',
                queryset=When.objects.filter(status='accepted')
            )
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


class EventAutocompleteView(ListAPIView):
    def get_queryset(self):
        term = self.request.GET.get("term") or ""
        queryset = Event.objects.filter(
            title__istartswith=term
        )
        return queryset

    serializer_class = EventAutocompleteSerializer


class EventSearchView(ListAPIView):
    def get_queryset(self):
        search = self.request.GET.get("search")
        queryset = Event.objects.annotate(
            search=SearchVector('description', 'title'),
        ).filter(search=search)
        return queryset

    serializer_class = EventRetrieveSerializer
