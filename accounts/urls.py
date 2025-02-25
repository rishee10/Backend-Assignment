# from os import path
from django.urls import path
from .views import ForgotPasswordView, LoginView, ReferralListView, ReferralStatsView, RegisterView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('referrals/', ReferralListView.as_view(), name='referrals'),
    path('referral-stats/', ReferralStatsView.as_view(), name='referral-stats'),
]
