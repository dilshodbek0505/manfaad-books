import hashlib
import hmac
import os

from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from apps.book.models import Book
from apps.book.api_endpoints.BookInfo.serializers import BookSerializer
from apps.users.models import User

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import StreamingHttpResponse

from wsgiref.util import FileWrapper


class BookWithGenerateAudioUrl(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookSerializer
    lookup_field = 'book_id'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

    def get(self, request, *args, **kwargs):
        user = self.request.user
        book_id = self.kwargs[self.lookup_field]

        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            raise NotFound('BookInfo not found')

        if book.is_premium and not user.is_premium:
            raise PermissionDenied("There is no access for this book")

        serializer = self.get_serializer(instance=book)

        return Response({"data": serializer.data}, status=200)


class BookWithoutGenerateAudioUrl(GenericAPIView):
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(pk=self.kwargs['user_id'])
        except ObjectDoesNotExist:
            raise NotFound('User not found')

        book_id = self.kwargs['book_id']
        book_url = self.kwargs['book_url']

        data = f"{user.id}:{book_id}"
        secret_ket = settings.SECRET_KEY.encode()
        url = hmac.new(secret_ket, data.encode(), hashlib.sha256).hexdigest()

        if book_url != url:
            raise PermissionDenied("There is no access for this book")

        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            raise NotFound('BookInfo not found')

        if book.is_premium and not user.is_premium:
            raise PermissionDenied("There is no access for this book")

        audio_path = book.file.path

        if not os.path.exists(audio_path):
            raise NotFound("File not found")

        audio_type = os.path.splitext(audio_path)[-1].lower().lstrip('.')
        content_type = f'audio/{audio_type}'

        file_wrapper = FileWrapper(open(audio_path, 'rb'))
        response = StreamingHttpResponse(file_wrapper, content_type=content_type)

        response['Content-Length'] = os.path.getsize(audio_path)
        response['Accept-Ranges'] = 'bytes'

        return response



