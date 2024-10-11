from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from rest_framework.response import Response
from rest_framework.generics import ListAPIView, DestroyAPIView, GenericAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.book.api_endpoints.Story.serializers import StoryUserSerializer, StorySaveUserSerializer
from apps.book.models import Story, StoryUser, StorySaveUser


class StoryListApi(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = StoryUserSerializer
    queryset = StoryUser.objects.all()
    pagination_class = None

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

    def get_queryset(self):
        stories = StoryUser.objects.filter(user=self.request.user, end_date__gte=timezone.now()).order_by('is_viewed', '-created_at')
        return stories


class StoryUpdateApi(GenericAPIView):
    serializer_class = StoryUserSerializer
    permission_classes = (IsAuthenticated,)
    queryset = StoryUser.objects.all()
    lookup_field = 'pk'

    def patch(self, request, *args, **kwargs):
        story_id = kwargs.get(self.lookup_field)
        try:
            story = StoryUser.objects.get(id=story_id)
            serializer = self.serializer_class(instance=story, data=self.request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"data": "ok"}, status=200)
        except ObjectDoesNotExist:
            return Response({"data": "not found"}, status=404)


class StorySaveUserListCreateApi(ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = StorySaveUser.objects.all()
    serializer_class = StorySaveUserSerializer
    pagination_class = None

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class StorySaveUserDeleteApi(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = StorySaveUser.objects.all()


__all__ = [
    'StoryListApi',
    'StoryUpdateApi',
    'StorySaveUserListCreateApi',
    'StorySaveUserDeleteApi',
]
