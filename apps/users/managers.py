from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import make_password


class CustomUserManager(BaseUserManager):
    def _create_user(self, phone_number, full_name, age, password, **extra_fields):
        """
        Create and save a user with the given phone_number, full_name, age and password.
        """
        if not phone_number:
            raise ValueError("The given username must be set")
        if not full_name:
            raise ValueError("The given full name must be set")
        if not age:
            raise ValueError("The given age must be set")

        user = self.model(phone_number=phone_number, full_name=full_name, age=age, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, full_name, age, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, full_name, age, password, **extra_fields)

    def create_superuser(self, phone_number, full_name, age, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, full_name, age, password, **extra_fields)