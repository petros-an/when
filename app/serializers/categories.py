from rest_framework import serializers
from app.models import Category


class CategoryRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

