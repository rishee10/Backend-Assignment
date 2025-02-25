from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Referral, Reward

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'referral_code', 'referred_by', 'created_at']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    referral_code = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'referral_code']

    def create(self, validated_data):
        referral_code = validated_data.pop('referral_code', None)
        referred_by = None
        if referral_code:
            referred_by = User.objects.filter(referral_code=referral_code).first()
        
        user = User.objects.create_user(**validated_data)  # Create user first
        
        if referred_by:
            user.referred_by = referred_by  # Assign referred_by separately
            user.save()  # Save after assigning
            Referral.objects.create(referrer=referred_by, referred_user=user, status='successful')

        return user


class ReferralSerializer(serializers.ModelSerializer):
    referrer = UserSerializer()
    referred_user = UserSerializer()
    class Meta:
        model = Referral
        fields = '__all__'
