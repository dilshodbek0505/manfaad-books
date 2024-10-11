from rest_framework.generics import ListAPIView

from apps.book.api_endpoints.Goal.serializers import GoalSerializer
from apps.book.models import Goal


class GoalListAPIView(ListAPIView):
    serializer_class = GoalSerializer
    queryset = Goal.objects.all()
    pagination_class = None


__all__ = [
    'GoalListAPIView',
]
