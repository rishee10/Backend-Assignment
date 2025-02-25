from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, UserSerializer, ReferralSerializer
from .models import Referral
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model

User = get_user_model()

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"user": UserSerializer(user).data, "tokens": get_tokens_for_user(user)}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            return Response({"user": UserSerializer(user).data, "tokens": get_tokens_for_user(user)})
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
            send_mail("Password Reset", f"Click here: {reset_link}", settings.DEFAULT_FROM_EMAIL, [email])
            return Response({"message": "Reset link sent"})
        except User.DoesNotExist:
            return Response({"error": "Email not found"}, status=status.HTTP_400_BAD_REQUEST)

class ReferralListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        referrals = Referral.objects.filter(referrer=request.user)
        return Response(ReferralSerializer(referrals, many=True).data)

class ReferralStatsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        total_referrals = Referral.objects.filter(referrer=request.user).count()
        successful_referrals = Referral.objects.filter(referrer=request.user, status='successful').count()
        return Response({"total_referrals": total_referrals, "successful_referrals": successful_referrals})