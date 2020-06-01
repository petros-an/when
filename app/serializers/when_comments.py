from rest_framework import serializers

from app.models import WhenComment


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
    class Meta:
        model = WhenComment
        fields = "__all__"