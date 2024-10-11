from rest_framework.authentication import BaseAuthentication

from apps.users.models import Token


class TokenAuthentication(BaseAuthentication):
    keyword = b'token'

    def get_header(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')

        if isinstance(auth_header, str):
            auth_header = auth_header.encode()

        return auth_header

    def authenticate(self, request):
        auth_header = self.get_header(request)

        if not auth_header:
            return None

        auth_header = auth_header.split()

        if len(auth_header) != 2 or auth_header[0].lower() != self.keyword:
            return None

        try:
            token = Token.objects.select_related("user").get(token=auth_header[1].decode("utf-8"))

        except Token.DoesNotExist:
            return None

        return (token.user, token)








