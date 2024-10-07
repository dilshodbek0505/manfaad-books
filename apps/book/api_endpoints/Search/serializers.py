from rest_framework import serializers

from apps.book.models import Book, Collection, Category
from apps.book.api_endpoints.BookInfo.serializers import BookSerializer


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ("id", "image")


class CategorySerializer(serializers.ModelSerializer):
    book_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ("id", "name", "icon", "book_count")

    def get_book_count(self, obj):
        book_count = Book.objects.filter(category=obj).count()
        return book_count


class SearchHomeSerializer(serializers.Serializer):
    categories = serializers.SerializerMethodField()
    books = serializers.SerializerMethodField()
    collections = serializers.SerializerMethodField()
    challenges = serializers.SerializerMethodField()

    def get_categories(self):
        categories = Category.objects.all()
        return CategorySerializer(instance=categories, many=True).data

    def get_books(self):
        books = Book.objects.all().order_by("-created_at")[:10]
        return BookSerializer(instance=books, many=True, context={'user': self.context.get('user')}).data

    def get_collections(self):
        collections = Collection.objects.all()
        return CollectionSerializer(instance=collections, many=True).data

    def get_challenges(self):
        return []

    @property
    def data(self):
        return {
            "categories": self.get_categories(),
            "books": self.get_books(),
            "collections": self.get_collections(),
            "challenges": self.get_challenges(),
        }

