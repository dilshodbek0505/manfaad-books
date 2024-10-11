from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.book.models import UserBookRating
from apps.book.api_endpoints.UserBookRating.serializers import UserBookRatingSerializer


class AddRating(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserBookRatingSerializer
    queryset = UserBookRating.objects.all()


__all__ = ['AddRating']