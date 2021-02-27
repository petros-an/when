from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from app.models import PropositionComment
from app.serializers import WhenCommentRetrieveSerializer, WhenCommentCreateSerializer
from app.views.mixins import AllowAnyForRead


class WhenCommentsViewSet(AllowAnyForRead, GenericViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin):
    def get_serializer_context(self):
        parent = super().get_serializer_context()
        parent.update({'when_id':self.kwargs['when_pk']})
        return parent

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return WhenCommentRetrieveSerializer
        else:
            return WhenCommentCreateSerializer

    def get_object(self):
        return get_object_or_404(PropositionComment, id=self.kwargs["pk"])

    def get_queryset(self):
        return PropositionComment.objects.filter(when_id=self.kwargs['when_pk'])