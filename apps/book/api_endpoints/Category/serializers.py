from rest_framework import serializers
from rest_framework.fields import empty

from apps.book.models import Category, Book


class CategorySerializer(serializers.ModelSerializer):
    book_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ("id", "name", "icon", "book_count")

    @staticmethod
    def get_book_count(obj):
        book_count = Book.objects.filter(category=obj).count()
        return book_count


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'icon')

