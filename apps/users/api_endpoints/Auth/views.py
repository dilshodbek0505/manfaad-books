from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from apps.users.api_endpoints.Auth.serializers import UserSerializer, OtpSerializer, ConfirmOtpSerializer, LoginSerializer
from apps.users.utiles import generate_code
from apps.users.models import User

from django.core.cache import cache
from django.contrib.auth import authenticate


class ConfirmOtpApi(GenericAPIView):
    serializer_class = ConfirmOtpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cache_code = cache.get(f'otp_{serializer.validated_data["phone_number"]}')

        if cache_code != serializer.validated_data["code"]:
            return Response({"data": "wrong_code"}, status=400)

        cache.delete(f'otp_{serializer.validated_data["phone_number"]}')

        return Response({"data": "ok"}, status=200)


class RegisterOtpApi(GenericAPIView):
    serializer_class = OtpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']
        if User.objects.filter(phone_number=phone_number).exists():
            return Response({"data": "phone_number already exists"}, status=400)

        if cache.keys(f'otp_{serializer.validated_data["phone_number"]}'):
            return Response({"data": "sms_already_send"}, status=400)

        code = generate_code()

        cache.set(f'otp_{serializer.validated_data["phone_number"]}', code, 60 * 2)
        print(code)

        return Response({"data": "send_code"}, status=200)


class LoginOtpApi(GenericAPIView):
    serializer_class = OtpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']

        if not User.objects.filter(phone_number=phone_number).exists():
            return Response({"data": "user not found"}, status=404)

        if cache.keys(f'otp_{serializer.validated_data["phone_number"]}'):
            print(cache.get(f'otp_{serializer.validated_data["phone_number"]}'))
            return Response({"data": "sms_already_send"}, status=400)

        code = generate_code()

        cache.set(f'otp_{serializer.validated_data["phone_number"]}', code, 60 * 2)
        print(code)

        return Response({"data": "send_code"}, status=200)


class UserRegisterApi(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        token, _ = Token.objects.get_or_create(user_id=serializer.data['id'])

        return Response({"token": token.key, "data": serializer.data}, status=200)


class UserLoginApi(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(self.request, phone_number = serializer.data['phone_number'], password = serializer.data['password'])
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            serializer = UserSerializer(instance=user)

            return Response({"token": token.key, "data": serializer.data}, status=200)
        else:
            return Response({"data": "user not found"}, status=404)


class UserDetailsApi(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user