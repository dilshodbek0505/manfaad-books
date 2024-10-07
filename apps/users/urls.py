from django.urls import path
from apps.users.api_endpoints.Auth.views import (
    UserLoginApi,
    UserRegisterApi,
    UserDetailsApi,
    ConfirmOtpApi,
    LoginOtpApi,
    RegisterOtpApi
)


urlpatterns = [
    # user api
    path('otp-login/', LoginOtpApi.as_view()),
    path('otp-register/', RegisterOtpApi.as_view()),
    path('login/', UserLoginApi.as_view()),
    path('register/', UserRegisterApi.as_view()),
    path('user-details/', UserDetailsApi.as_view()),
    path('confirm-otp/', ConfirmOtpApi.as_view()),

]