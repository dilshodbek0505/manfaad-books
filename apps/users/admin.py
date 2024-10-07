from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin

from apps.users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = ("phone_number", "full_name", "is_deleted", "is_premium")