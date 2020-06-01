from rest_framework import viewsets

from app.models import Category
from app.serializers.categories import CategoryRetrieveSerializer


class CategoriesViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategoryRetrieveSerializer
    queryset = Category.objects.all()
