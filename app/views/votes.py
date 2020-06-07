from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet

from app.models import Vote
from app.serializers import VoteRetrieveSerializer, VoteCreateSerializer
from app.views import AllowAnyForRead


class WhenVotesViewset(AllowAnyForRead, GenericViewSet, CreateModelMixin, ListModelMixin):

    def get_serializer_class(self):
        if self.action == 'list':
            return VoteRetrieveSerializer
        elif self.action == 'create':
            return VoteCreateSerializer

    def get_serializer_context(self):
        parent = super().get_serializer_context()
        parent.update({'when_id':self.kwargs['when_pk']})
        return parent

    def get_queryset(self):
        return Vote.objects.filter(
            when_id=self.kwargs["when_pk"]
        )


