from rest_framework.response import Response
from rest_framework import filters
from rest_framework.generics import ListAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated

from apps.book.api_endpoints.BookInfo.serializers import BookSerializer
from apps.book.api_endpoints.Search.serializers import SearchHomeSerializer, EmptySerializer
from apps.book.models import Book


class SearchHomeApi(GenericAPIView):
    serializer_class = EmptySerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        serializer = SearchHomeSerializer(context={'user': self.request.user})
        return Response({"data": serializer.data})


class SearchDataApi(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ['category__name', 'author__full_name', 'slug']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context


__all__ = ['SearchHomeApi', 'SearchDataApi']