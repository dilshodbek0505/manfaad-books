from rest_framework import serializers

from apps.book.api_endpoints.BookInfo.serializers import BookSerializer
from apps.book.models import Story, StoryUser, StorySaveUser


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
    is_saved = serializers.SerializerMethodField()

    class Meta:
        model = StoryUser
        fields = ('id', 'story', 'is_viewed', 'is_saved')

    def get_is_saved(self, obj):
        user = self.context.get('user')
        return StorySaveUser.objects.filter(user=user, story=obj.story).exists()


    def get_story(self, obj):
        user = self.context.get('user')
        return StorySerializer(instance=obj.story, context={'user': user}).data


class StorySaveUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = StorySaveUser
        fields = ("id","story", "user")
        extra_kwargs = {'user': {'required': False}}
        
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        user = self.context.get('user')

        data['story'] = StorySerializer(instance=instance.story, context={'user': user}).data
        return data

    