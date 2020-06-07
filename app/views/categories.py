from rest_framework import viewsets

from app.models import Category
from app.serializers.categories import CategoryRetrieveSerializer
from app.views.mixins import AllowAnyForRead


class CategoriesViewset(AllowAnyForRead, viewsets.ReadOnlyModelViewSet):
    serializer_class = CategoryRetrieveSerializer
    queryset = Category.objects.all()
