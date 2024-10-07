from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from apps.book.api_endpoints.HomePage.serializers import HomeSerializer, EmptySerializer


class HomePage(GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = EmptySerializer

    def get(self, request, *args, **kwargs):
        serializer = HomeSerializer(context={'user': self.request.user})
        return Response(serializer.data)
