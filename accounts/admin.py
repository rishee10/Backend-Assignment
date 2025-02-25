from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Referral, Reward

# Extend Django's built-in UserAdmin for customization
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'referral_code', 'referred_by', 'created_at')
    search_fields = ('username', 'email', 'referral_code')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

# Register the models
admin.site.register(User, CustomUserAdmin)
admin.site.register(Referral)
admin.site.register(Reward)

