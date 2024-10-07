from rest_framework import serializers

from apps.book.models import Category, Book


class CategorySerializer(serializers.ModelSerializer):
    book_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ("id", "name", "icon", "book_count")

    def get_book_count(self, obj):
        book_count = Book.objects.filter(category=obj).count()
        return book_count
