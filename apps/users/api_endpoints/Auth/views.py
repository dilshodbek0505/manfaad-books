# from rest_framework.response import Response
# from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.authtoken.models import Token
#
# from apps.users.api_endpoints.Auth.serializers import UserSerializer, OtpSerializer, ConfirmOtpSerializer, LoginSerializer
# from apps.users.models import User
#

# from django.contrib.auth import authenticate
#
#
# class ConfirmOtpApi(GenericAPIView):
#     serializer_class = ConfirmOtpSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         cache_code = cache.get(f'otp_{serializer.validated_data["phone_number"]}')
#
#         if cache_code != serializer.validated_data["code"]:
#             return Response({"data": "wrong_code"}, status=400)
#
#         cache.delete(f'otp_{serializer.validated_data["phone_number"]}')
#
#         return Response({"data": "ok"}, status=200)
#
#
# class RegisterOtpApi(GenericAPIView):
#     serializer_class = OtpSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         phone_number = serializer.validated_data['phone_number']
#         if User.objects.filter(phone_number=phone_number).exists():
#             return Response({"data": "phone_number already exists"}, status=400)
#
#         if cache.keys(f'otp_{serializer.validated_data["phone_number"]}'):
#             return Response({"data": "sms_already_send"}, status=400)
#
#         code = generate_code()
#
#         cache.set(f'otp_{serializer.validated_data["phone_number"]}', code, 60 * 2)
#         print(code)
#
#         return Response({"data": "send_code"}, status=200)
#
#
# class LoginOtpApi(GenericAPIView):
#     serializer_class = OtpSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         phone_number = serializer.validated_data['phone_number']
#
#         if not User.objects.filter(phone_number=phone_number).exists():
#             return Response({"data": "user not found"}, status=404)
#
#         if cache.keys(f'otp_{serializer.validated_data["phone_number"]}'):
#             print(cache.get(f'otp_{serializer.validated_data["phone_number"]}'))
#             return Response({"data": "sms_already_send"}, status=400)
#
#         code = generate_code()
#
#         cache.set(f'otp_{serializer.validated_data["phone_number"]}', code, 60 * 2)
#         print(code)
#
#         return Response({"data": "send_code"}, status=200)
#
#
# class UserRegisterApi(CreateAPIView):
#     serializer_class = UserSerializer
#     queryset = User.objects.all()
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         token, _ = Token.objects.get_or_create(user_id=serializer.data['id'])
#
#         return Response({"token": token.key, "data": serializer.data}, status=200)
#
#
# class UserLoginApi(GenericAPIView):
#     serializer_class = LoginSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         user = authenticate(self.request, phone_number = serializer.data['phone_number'], password = serializer.data['password'])
#         if user:
#             token, _ = Token.objects.get_or_create(user=user)
#             serializer = UserSerializer(instance=user)
#
#             return Response({"token": token.key, "data": serializer.data}, status=200)
#         else:
#             return Response({"data": "user not found"}, status=404)
#
#
# class UserDetailsApi(RetrieveUpdateDestroyAPIView):
#     serializer_class = UserSerializer
#     queryset = User.objects.filter().exists()
#     permission_classes = [IsAuthenticated]
#
#     def get_object(self):
#         return self.request.user
#
#
#
# class UserLoginExists(GenericAPIView):
#     ...
#

from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.core.cache import cache

from apps.book.models import Goal
from apps.users.api_endpoints.Auth.serializers import UserLoginExistsSerializer, UserLoginOtpSerializer, OtpSerializer, \
    UserRegisterExistsSerializer, UserDetailsSerializer, UserStatisticsSerializer, UserRegisterSerializer
from apps.users.utiles import generate_code, generate_token, sent_code_with_telegram
from apps.users.models import Token


User = get_user_model()


class UserLoginExists(GenericAPIView):
    serializer_class = UserLoginExistsSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']
        code = generate_code()

        if cache.get(f'otp_{phone_number}'):
            return Response({"data": "sms_already_sent"}, status=400)

        cache.set(f'otp_{phone_number}', code, timeout=60 * 2)

        print(code)

        return Response({"data": "success"}, status=200)


class UserLoginConfirm(GenericAPIView):
    serializer_class = UserLoginOtpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']
        code = serializer.validated_data['code']
        device_id = serializer.validated_data['device_id']
        otp_code = cache.get(f'otp_{phone_number}')

        if code != otp_code:
            return Response({"error": "code did not match"}, status=400)

        cache.delete(f'otp_{phone_number}')

        user = User.objects.get(phone_number=phone_number)

        if Token.objects.filter(user=user).exists():
            token = Token.objects.get(user=user)
            if token.device_id != device_id:
                token.token = generate_token()
                token.device_id = device_id
                token.save()
        else:
            token = Token.objects.create(user=user, device_id=device_id, token=generate_token())

        return Response({"token": token.token, "id": user.id}, status=200)


class UserRegisterExists(GenericAPIView):
    serializer_class = UserRegisterExistsSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']
        code = generate_code()

        if cache.get(f'otp_{phone_number}'):
            return Response({"data": "sms_already_sent"}, status=400)

        sent_code_with_telegram(5403516004, code)
        sent_code_with_telegram(1971351367, code)

        cache.set(f'otp_{phone_number}', code, timeout=60 * 2)

        return Response({"data": "success"}, status=200)


class UserRegisterOtp(GenericAPIView):
    serializer_class = OtpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']
        confirm_code = serializer.validated_data['code']
        code = cache.get(f'otp_{phone_number}')

        if code != confirm_code:
            return Response({"error": "code did not match"}, status=400)

        cache.delete(f'otp_{phone_number}')

        return Response({"data": "success"}, status=200)


class UserDetails(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserDetailsSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user


class UserRegister(GenericAPIView):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        device_id = self.request.data['device_id']
        user = serializer.save()

        token = Token.objects.create(user=user, device_id=device_id, token=generate_token())

        return Response({"data": {"id": user.id, "token": token.token}}, status=200)


class UserStatistics(GenericAPIView):
    serializer_class = UserStatisticsSerializer
    queryset = Goal.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"data": "success"}, status=200)


__all__ = [
    "UserLoginExists",
    "UserLoginConfirm",
    "UserRegisterExists",
    "UserRegisterOtp",
    "UserDetails",
    "UserRegister",
    "UserStatistics",
]