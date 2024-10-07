from rest_framework import serializers
from rest_framework.exceptions import NotFound

from apps.book.models import Book, BookChapter, BookSave

from django.conf import settings

import hmac
import hashlib


class BookChapterSerializer(serializers.ModelSerializer):
    point = serializers.SerializerMethodField()

    class Meta:
        model = BookChapter
        fields = ("title", "chapter", "point")

    @staticmethod
    def get_point(obj):
        return obj.point.total_seconds()


class BookSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    chapters = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()
    file = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ("id", "title", "slug", "duration", "file", "category", "author", "img", "like_count", "description", "is_premium", "what_is_learned", "chapters", "is_saved")

    def get_is_saved(self, obj):
        user = self.context.get('user')
        return BookSave.objects.filter(user=user, book=obj).exists()

    @staticmethod
    def get_chapters(obj):
        book_chapters = BookChapter.objects.filter(book=obj)
        return BookChapterSerializer(book_chapters, many=True).data

    @staticmethod
    def get_duration(obj):
        minutes, seconds = divmod(int(obj.duration.total_seconds()), 60)
        return f'{minutes:02d}:{seconds:02d}'

    @staticmethod
    def get_author(obj):
        return {
            "full_name": obj.author.full_name,
            "about": obj.author.about,
        }

    @staticmethod
    def get_category(obj):
        return {
            "name": obj.category.name,
            "icon": obj.category.icon.url,
        }

    def get_file(self, obj):
        user = self.context.get('user')
        book = obj

        if not user:
            raise NotFound('User does not exist')

        data = f"{user.id}:{book.id}"

        secret_key = settings.SECRET_KEY.encode()

        url = hmac.new(secret_key, data.encode(), hashlib.sha256).hexdigest()

        return url
