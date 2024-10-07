from rest_framework import serializers

from apps.book.models import UserBookRating


class UserBookRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBookRating
        fields = ("id", "user", "book", "is_liked")