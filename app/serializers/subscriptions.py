from django.db import IntegrityError
from rest_framework import serializers

from app.models import Subscription
from app.serializers import EventRetrieveSerializer


class SubscriptionRetrieveSerializer(serializers.ModelSerializer):
    event = EventRetrieveSerializer()

    class Meta:
        model = Subscription
        fields = "__all__"


class SubscriptionCreateSerializer(serializers.ModelSerializer):
    config = serializers.JSONField(required=True, allow_null=False)
    method = serializers.ChoiceField(choices=Subscription.SUBSCRIPTION_CHOICES, default='email')

    class Meta:
        model = Subscription
        fields = ["config", "method"]

    def validate_config(self, config):
        notification_intervals = Subscription.NOTIFICATION_INTERVALS
        res = {}
        for key, value in config.items():
            try:
                assert key in notification_intervals
                assert value
                res[key] = value
            except AssertionError:
                raise serializers.ValidationError(f"Config '{key}:{value}' not understood")
        if not res:
            raise serializers.ValidationError(f"At least one of {notification_intervals} must be provided")
        return res

    def create(self, validated_data):
        validated_data.update({
            "user": self.context['request'].user,
            "event_id": self.context["event_id"],
        })
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError("Event not found")