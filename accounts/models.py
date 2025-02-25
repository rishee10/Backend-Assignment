from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
import uuid
from django.urls import path
# from .views import RegisterView, LoginView, ForgotPasswordView, ReferralListView, ReferralStatsView

class User(AbstractUser):
    email = models.EmailField(unique=True)
    referral_code = models.CharField(max_length=10, unique=True, blank=True, null=True)
    referred_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals')
    created_at = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_groups",
        blank=True
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions",
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = str(uuid.uuid4())[:10]
        super().save(*args, **kwargs)


class Referral(models.Model):
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_referrals')
    referred_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_referral')
    date_referred = models.DateTimeField(default=now)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('successful', 'Successful')], default='pending')

class Reward(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    reason = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)