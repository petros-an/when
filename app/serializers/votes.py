from django.db import IntegrityError
from django.db.models import F
from rest_framework import serializers

from app.models import Vote, Proposition


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
        increment = 1 if sentiment == 'up' else -1
        try:
            vote = Vote.objects.get(
                user=validated_data['user'],
                when_id=self.context['when_id'],
            )
            if vote.sentiment != sentiment:
                vote.sentiment = sentiment
                vote.save()
                Proposition.objects.filter(id=self.context['when_id']).update(score=F('score') + increment * 2)
        except Vote.DoesNotExist:
            vote = Vote.objects.create(
                user=validated_data['user'],
                when_id=self.context['when_id'],
                sentiment=sentiment
            )
            Proposition.objects.filter(id=self.context['when_id']).update(score=F('score') + increment)
        return vote
