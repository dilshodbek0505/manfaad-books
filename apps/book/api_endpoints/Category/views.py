from rest_framework.response import Response
from rest_framework.generics import ListAPIView, GenericAPIView

from apps.book.api_endpoints.Category.serializers import CategorySerializer, CategoryListSerializer
from apps.book.models import Category


class CategoryListAPIView(ListAPIView):
    serializer_class = CategoryListSerializer
    queryset = Category.objects.all()
    pagination_class = None


__all__ = [
    'CategoryListAPIView',
]







