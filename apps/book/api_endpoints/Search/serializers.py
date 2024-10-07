from rest_framework import serializers

from apps.book.models import Book, Collection, Category
from apps.book.api_endpoints.BookInfo.serializers import BookSerializer
from apps.book.api_endpoints.Category.serializers import CategorySerializer
from apps.book.api_endpoints.Collection.serializers import CollectionSerializer


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


class EmptySerializer(serializers.Serializer):
    class Meta:
        ref_name = "SearchEmptySerializer"