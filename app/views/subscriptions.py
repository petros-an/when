from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet

from app.models import Subscription
from app.serializers.subscriptions import SubscriptionRetrieveSerializer, SubscriptionCreateSerializer
from app.views.mixins import DisplayErrorMixin


class SubscriptionViewSet(GenericViewSet, ListModelMixin):
    serializer_class = SubscriptionRetrieveSerializer

    def get_queryset(self):
        return Subscription.objects.filter(
            user_id=self.request.user.id
        ).order_by("-created")


class EventSubscriptionViewSet(DisplayErrorMixin, GenericViewSet, CreateModelMixin):

    serializer_class = SubscriptionCreateSerializer
    queryset = Subscription.objects.all()

    def get_serializer_context(self):
        parent = super().get_serializer_context()
        parent.update({
            'event_id': self.kwargs['event_pk']
        })
        return parent


