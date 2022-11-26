from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import AdminPasswordChangeForm

from core.models import User


# Register your models here.

@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name")
    list_filter = ("is_staff", "is_active", "is_superuser")
    search_fields = ("email", "first_name", "last_name", "username")
    readonly_fields = ("date_joined", "last_login")
    exclude = ("groups", "user_permissions", "is_superuser")
    fieldsets = ()

