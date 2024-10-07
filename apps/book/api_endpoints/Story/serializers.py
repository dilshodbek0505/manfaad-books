from rest_framework import serializers

from apps.book.api_endpoints.BookInfo.serializers import BookSerializer
from apps.book.models import Story, StoryUser


class StorySerializer(serializers.ModelSerializer):
    book = serializers.SerializerMethodField()

    class Meta:
        model = Story
        fields = ('id', 'image', 'title', 'book', 'context')

    def get_book(self, obj):
        user = self.context.get('user')
        return BookSerializer(obj.book, context={'user': user}).data


class StoryUserSerializer(serializers.ModelSerializer):
    story = serializers.SerializerMethodField()

    class Meta:
        model = StoryUser
        fields = ('id', 'story', 'is_viewed')

    def get_story(self, obj):
        user = self.context.get('user')
        return StorySerializer(instance=obj.story, context={'user': user}).data

