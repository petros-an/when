from rest_framework import serializers

from app.models import When


class WhenRetrieveSerializer(serializers.ModelSerializer):
    when = serializers.DateTimeField()

    class Meta:
        model = When
        fields = '__all__'


class WhenCreateSerializer(serializers.ModelSerializer):
    when = serializers.DateTimeField()
    description = serializers.CharField(max_length=200)
    sources = serializers.JSONField()

    def create(self, validated_data):
        validated_data["event_id"] = self.context["view"].kwargs["event_pk"]
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = When
        fields = ["when", "description", "sources"]


class WhenUpdateSerializer(serializers.ModelSerializer):
    when = serializers.DateTimeField()
    description = serializers.CharField(max_length=200, required=False)
    sources = serializers.JSONField(required=False)

    def update(self, instance, validated_data):
        if self.context['request'].user.id != instance.user_id:
            raise serializers.ValidationError("Can only change your own whens")
        super().update(instance, validated_data)

    class Meta:
        model = When
        fields = ["when", "description", "sources"]
