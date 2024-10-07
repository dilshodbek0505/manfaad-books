from rest_framework import serializers

from apps.book.models import Collection


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ("id", "image")