from django.contrib.postgres.search import SearchVector
from django.db.models import Prefetch, Count, Q
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.decorators import action, authentication_classes, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from app.models import Event, When
from app.serializers.events import EventRetrieveSerializer, EventCreateSerializer, EventUpdateSerializer, \
    EventAutocompleteSerializer
from app.views.mixins import AllowAnyForRead


class EventViewset(AllowAnyForRead, viewsets.ModelViewSet):

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
        return qs.order_by("-created")

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


class EventAutocompleteView(AllowAnyForRead, ListAPIView):

    def get_queryset(self):
        term = self.request.GET.get("term") or ""
        queryset = Event.objects.filter(
            title__istartswith=term
        )
        return queryset

    serializer_class = EventAutocompleteSerializer


class EventSearchView(AllowAnyForRead, ListAPIView):
    permission_classes = (AllowAny,)

    def get_queryset(self):
        search = self.request.GET.get("term")
        queryset = Event.objects.annotate(
            search=SearchVector('description', 'title'),
        ).filter(Q(search=search) | Q(title__istartswith=search))
        return queryset

    serializer_class = EventRetrieveSerializer
