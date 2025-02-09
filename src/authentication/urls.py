from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from src.authentication.apis.auth.confirm_otp_code import ConfirmOtpCodeApi
from src.authentication.apis.auth.resend_otp_code import ReSendOtpCodeApi
from src.authentication.apis.auth.sign_in_up import SignInUpApi

urlpatterns = [
    path('refresh-jwt/', TokenRefreshView.as_view(), name="refresh"),
    path('verify-jwt/', TokenVerifyView.as_view(), name="verify"),

    path('sign-in-up/', SignInUpApi.as_view(), name='sign-in-up'),
    path('resend-otp-code/', ReSendOtpCodeApi.as_view(), name='resend-otp'),
    path('confirm-otp-code/', ConfirmOtpCodeApi.as_view(), name='confirm-verification-code'),
]
