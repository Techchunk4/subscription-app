from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'subscription_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Subscription', {'fields': ('stripe_customer_id', 'subscription_active')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

admin.site.register(User, CustomUserAdmin)