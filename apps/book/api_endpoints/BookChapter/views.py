from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from apps.book.api_endpoints.BookChapter.serializers import BookChapterSerializer
from apps.book.models import Book, BookChapter


class BookChapterRetrieve(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookChapterSerializer
    queryset = Book.objcets.all()
    lookup_field = 'pk'


__all__ = [
    'BookChapterRetrieve',
]