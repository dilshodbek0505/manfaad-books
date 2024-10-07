from rest_framework import serializers

from apps.book.models import Book, BookChapter


class BookChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "author", "rating", "description", "img", "duration", "is_premium", "what_is_learned", "category")



