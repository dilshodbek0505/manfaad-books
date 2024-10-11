from django.urls import path

from .api_endpoints import *

app_name = 'users'


urlpatterns = [
    path('login/', UserLoginExists.as_view(), name='login'),
    path('login/confirm/', UserLoginConfirm.as_view(), name='login-otp'),
    path('register/exists/', UserRegisterExists.as_view(), name='register-exists'),
    path('register/confirm/', UserRegisterOtp.as_view(), name='register-otp'),
    path('register/', UserRegister.as_view(), name='register'),
    path('user/statistics/', UserStatistics.as_view(), name='statistics'),
    path('user/details/', UserDetails.as_view(), name='user-details'),

]

