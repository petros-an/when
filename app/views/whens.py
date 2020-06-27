from django.contrib.postgres.search import SearchVector
from django.db.models import Exists, OuterRef
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied

from app.models import When, Event, PowerUser, Vote
from app.serializers.whens import WhenRetrieveSerializer, WhenCreateSerializer, WhenUpdateSerializer
from app.tasks import initiate_notifications_for_prevalent_when_change
from app.views.mixins import AllowAnyForRead


class EventWhenViewset(AllowAnyForRead, viewsets.ModelViewSet):

    def get_queryset(self):
        qs = When.objects.filter(event_id=self.kwargs["event_pk"])
        if self.request.user.is_authenticated:
            qs = qs.annotate(
                voted=Exists(
                    Vote.objects.filter(
                        user_id=self.request.user.id,
                        when_id=OuterRef("id")
                    )
                )
            )
        return qs

    def get_serializer(self, *args, **kwargs):
        context = self.get_serializer_context()
        if self.action == 'list' or self.action == 'retrieve':
            return WhenRetrieveSerializer(*args, **kwargs, context=context)
        elif self.action == 'create':
            return WhenCreateSerializer(*args, **kwargs, context=context)
        elif self.action == 'update' or self.action == 'partial_update':
            return WhenUpdateSerializer(*args, **kwargs, context=context)

    @action(detail=True, methods=["POST"], url_path="choose")
    def choose(self, request, *args, **kwargs):
        try:
            when = When.objects.select_related("event").get(
                event_id=self.kwargs["event_pk"],
                id=self.kwargs["pk"]
            )
        except When.DoesNotExist:
            raise Http404

        # if not PowerUser.objects.filter(user_id=request.user_id).exists():
        #     raise PermissionDenied("Only Power users can choose")
        when.event.prevalent_when = when
        when.event.save()
        initiate_notifications_for_prevalent_when_change.apply_async(when.event.id)
        return JsonResponse(status=200, data={})








