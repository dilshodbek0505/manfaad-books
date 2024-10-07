from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from apps.users.managers import CustomUserManager

from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractBaseUser, BaseModel, PermissionsMixin):
    full_name = models.CharField(max_length=255, help_text=_("User's full name."))
    phone_number = PhoneNumberField(blank=True, region="UZ", help_text=_("User's phone number."), unique=True)
    age = models.PositiveIntegerField(help_text=_("User's age."))
    avatar = models.ImageField(default="default.jpg", upload_to="users_avatar/", help_text=_("User's avatar."))

    is_premium = models.BooleanField(default=False, help_text=_("User is premium."))
    is_staff = models.BooleanField(default=False, help_text=_("User is staff."))
    is_deleted = models.BooleanField(default=False, help_text=_("User is deleted."))
    is_superuser = models.BooleanField(default=False, help_text=_("User is superuser."))

    objects = CustomUserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = [
        "full_name",
        "age"
    ]

    def __str__(self):
        return self.full_name

