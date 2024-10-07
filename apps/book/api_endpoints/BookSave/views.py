from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated

from apps.book.models import BookSave, UserBookRating
from apps.book.api_endpoints.BookSave.serializers import BookSaveSerializer, BookSaveListSerializer, \
    BookLikedSerializer

from rest_framework.generics import GenericAPIView, UpdateAPIView, ListAPIView
from rest_framework.response import Response


class BookSaveApi(GenericAPIView):
    serializer_class = BookSaveSerializer
    permission_classes = [IsAuthenticated]
    queryset = BookSave.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"data": "book_saved"}, status=200)

    def delete(self, request, *args, **kwargs):
        book_id = self.kwargs['pk']
        try:
            book_save = BookSave.objects.get(id=book_id)
            book_save.delete()
            return Response({"data": "ok"}, status=200)
        except ObjectDoesNotExist:
            return Response({"data": "book_not_found"}, status=404)


class BookSaveListApi(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookSaveListSerializer
    queryset = BookSave.objects.all()

    def get(self, request, *args, **kwargs):
        user = self.request.user
        book_save = BookSave.objects.filter(user=user)
        serializer = self.serializer_class(instance=book_save, many=True)
        return Response({"data": serializer.data}, status=200)


class BookLikedUpdateApi(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = BookLikedSerializer
    queryset = UserBookRating.objects.all()


class BookLikedListApi(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = BookLikedSerializer
    pagination_class = None

    def get_queryset(self):
        return UserBookRating.objects.filter(user = self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context