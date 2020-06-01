from rest_framework import serializers

from app.models import Vote


class VoteRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = "__all__"


class VoteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = []

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return Vote.objects.get_or_create(**validated_data)
