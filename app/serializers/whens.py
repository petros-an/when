import datetime

from rest_framework import serializers

from app.models import When, Vote


class WhenRetrieveSerializer(serializers.ModelSerializer):
    when = serializers.SerializerMethodField()
    voted = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context['request']
        if request.user.is_authenticated:
            votes = Vote.objects.filter(user_id=request.user.id).values_list("when_id", "sentiment")
            self.votes = {}
            for when_id, sentiment in votes:
                self.votes[when_id] = sentiment
        else:
            self.votes = {}

    def get_when(self, obj):
        return int(obj.when.timestamp())

    def get_voted(self, obj):
        return self.votes.get(obj.id, None)

    class Meta:
        model = When
        fields = '__all__'


class WhenStringSerializer(serializers.ModelSerializer):
    when = serializers.DateTimeField()

    class Meta:
        model = When
        fields = ["when"]




class WhenCreateSerializer(serializers.ModelSerializer):
    when = serializers.JSONField()
    description = serializers.CharField(max_length=200)

    @staticmethod
    def first_month_of_season(season):
        try:
            return {
                "spring": 3,
                "winter": 12,
                "summer": 6,
                "fall": 9
            }[season]
        except KeyError:
            raise serializers.ValidationError("unknown season")

    def validate_when(self, when):
        values = {
            "year": None,
            "season": None,
            "month": None,
            "day": None
        }
        specificity = "year"
        for interval in values.keys():
            value = when.get(interval)
            if value:
                specificity = interval
                values[interval] = value
            else:
                break
        try:
            if specificity == "season":
                dt = datetime.datetime(
                    year=int(values.get("year", 0)),
                    month=self.first_month_of_season(values['season']),
                    day=0
                )
            else:
                dt = datetime.datetime(
                    year=int(values.get("year", 1) or 1),
                    month=int(values.get("month", 1) or 1),
                    day=int(values.get("day", 1) or 1)
                )
        except ValueError:
            raise serializers.ValidationError("Invalid date")
        now = datetime.datetime.now()
        try:
            if specificity == 'year':
                assert dt.year >= now.year
            elif specificity == 'month':
                assert dt.year >= now.year and dt.month >= now.month
            elif specificity == 'season':
                assert dt.year >= now.year and self.first_month_of_season(values["season"]) >= now.month
            elif specificity == 'day':
                assert dt.year >= now.year and dt.month >= now.month and dt.day > now.day

        except AssertionError:
            raise serializers.ValidationError("Date must be in the future")
        self.specificity = specificity
        return dt

    def create(self, validated_data):
        validated_data["specificity"] = self.specificity
        validated_data["event_id"] = self.context["view"].kwargs["event_pk"]
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = When
        fields = ["when", "description", "specificity"]


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
