from rest_framework import serializers

from apps.book.models import Goal
from apps.book.api_endpoints.Category.serializers import CategoryListSerializer


class GoalSerializer(serializers.ModelSerializer):
    categories = CategoryListSerializer(many=True, read_only=True)

    class Meta:
        model = Goal
        fields = ('id', 'name', 'categories')

