from rest_framework import serializers

from app.models import Event, Category
from app.serializers.whens import WhenRetrieveSerializer


class EventRetrieveSerializer(serializers.ModelSerializer):
    whens = serializers.SerializerMethodField()
    prevalent_when = serializers.SerializerMethodField()

    def get_prevalent_when(self, obj):
        try:
            return WhenRetrieveSerializer(context=self.context).to_representation(obj.prevalent_when)
        except AttributeError:
            return None

    def get_whens(self, obj):
        return WhenRetrieveSerializer(many=True, context=self.context).to_representation(obj.whens)

    class Meta:
        model = Event
        fields = "__all__"


class EventAutocompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "title", "category"]


class EventCreateSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = Event
        fields = ["title", "description", "category"]


class EventUpdateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=40, required=False)
    description = serializers.CharField(max_length=200, required=False)
    category = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='slug')

    class Meta:
        model = Event
        fields = ["title", "description", "category"]
