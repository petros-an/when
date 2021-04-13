from django.contrib.postgres.search import SearchVector
from django.db.models import Prefetch, Q, Count
from rest_framework import viewsets
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework import parsers
from rest_framework.permissions import AllowAny

from app.models import Topic, Update
from app.serializers.events import EventRetrieveSerializer, EventCreateSerializer, EventUpdateSerializer, \
    EventAutocompleteSerializer, EventDetailSerializer
from app.views.mixins import AllowAnyForRead


class EventViewSet(AllowAnyForRead, viewsets.ModelViewSet):
    parser_classes = (parsers.JSONParser, parsers.MultiPartParser)

    def get_queryset(self):
        prefetch_qs = Update.objects.filter(Q(status='accepted') | Q(user_id=self.request.user.id)).annotate(comment_count=Count("when_comments"))
        qs = Topic.objects.filter(Q(status='accepted') | Q(user_id=self.request.user.id)).prefetch_related(
            Prefetch(
                'whens',
                queryset=prefetch_qs
            )
        )
        category = self.kwargs.get('category')
        if category:
            qs = qs.filter(category=category)
        return qs.order_by("-created")

    def get_serializer(self, *args, **kwargs):
        context = self.get_serializer_context()
        if self.action == 'list':
            return EventRetrieveSerializer(*args, **kwargs, context=context)
        elif self.action == 'retrieve':
            return EventDetailSerializer(*args, **kwargs, context=context)
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
        queryset = Topic.objects.filter(
            title__istartswith=term
        )
        return queryset

    serializer_class = EventAutocompleteSerializer


class EventSearchView(AllowAnyForRead, ListAPIView):
    permission_classes = (AllowAny,)

    def get_queryset(self):
        search = self.request.GET.get("term")
        if not search:
            return Topic.objects.none()
        queryset = Topic.objects.annotate(
            search=SearchVector('title'),
        ).filter(Q(search=search) | Q(title__istartswith=search))
        return queryset

    serializer_class = EventRetrieveSerializer


class SubmittedEventsView(ListAPIView):

    serializer_class = EventRetrieveSerializer

    def get_queryset(self):
        return Topic.objects.filter(user_id=self.request.user.id)
