from rest_framework import serializers

from app.models import WhenComment
from app.serializers.auth import UserSerializerMini


class WhenCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhenComment
        fields = ["text"]

    def create(self, validated_data):
        validated_data.update({
            "user": self.context['request'].user,
            "when_id": self.context['when_id']
        })
        return super().create(validated_data)


class WhenCommentRetrieveSerializer(serializers.ModelSerializer):
    user = UserSerializerMini()

    created = serializers.SerializerMethodField()
    def get_created(self, obj):
        return obj.created.timestamp() * 1000

    class Meta:
        model = WhenComment
        fields = ["created", "text", "id", "user"]