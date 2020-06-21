from django.db import IntegrityError
from django.db.models import F
from rest_framework import serializers

from app.models import Vote, When


class VoteRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = "__all__"


class VoteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ["sentiment"]

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        sentiment = validated_data['sentiment']
        try:
            vote, created = Vote.objects.update_or_create(
                user=validated_data['user'],
                when_id=self.context['when_id'],
                defaults={'sentiment': sentiment}
            )
        except IntegrityError:
            return Vote.objects.get(
                user_id=validated_data['user'].id,
                when_id=self.context['when_id'],
                sentiment=sentiment
            )
        if sentiment == 'up':
            When.objects.filter(id=self.context['when_id']).update(score=F('score') + 1)
        else:
            When.objects.filter(id=self.context['when_id']).update(score=F('score') - 1)
        return vote
