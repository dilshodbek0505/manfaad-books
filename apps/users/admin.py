from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin

from apps.users.models import User, Token


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (_("Personal info"),  {
            'fields': ('full_name', 'phone_number', 'avatar', 'age')
        }),
        (_("Security info"), {
            'fields': ('password', "last_login", "created_at")
        }),
        (_("Permissions"), {
            'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions', 'is_premium')
        }),
    )
    list_display = ("phone_number", "full_name", "is_deleted", "is_premium")
    readonly_fields = ("password", "last_login", "created_at", 'age')


admin.site.register(Token)

