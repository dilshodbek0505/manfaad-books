from rest_framework import serializers

from apps.book.models import BookSave, UserBookRating
from apps.book.api_endpoints.BookInfo.serializers import BookSerializer


class BookSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookSave
        fields = ("book", "user")


class BookSaveListSerializer(serializers.ModelSerializer):
    book = serializers.SerializerMethodField()

    class Meta:
        model = BookSave
        fields = ("id", "book")

    def get_book(self, obj):
        user = self.context.get('user')
        return BookSerializer(instance=obj.book, context={'user': user}).data
    

class BookLikedSerializer(serializers.ModelSerializer):
    book = serializers.SerializerMethodField()

    class Meta:
        model = UserBookRating
        fields = ("id", "book", "is_liked")
    

    def get_book(self, obj):
        user = self.context.get('user')
        return BookSerializer(instance = obj.book, context={'user': user}).data
    

    
    