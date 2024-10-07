from rest_framework import serializers

from django.core.validators import MinLengthValidator, MaxLengthValidator

from apps.users.models import User

from phonenumber_field.serializerfields import PhoneNumberField


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_deleted = serializers.BooleanField(read_only=True)
    is_premium = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'phone_number', 'full_name', 'avatar', 'age', 'password', 'is_deleted', 'is_premium')

    def save(self, **kwargs):
        user = super(UserSerializer, self).save(**kwargs)
        user.set_password(self.validated_data['password'])
        user.save()
        return user


class OtpSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(region='UZ')


class ConfirmOtpSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(region='UZ')
    code = serializers.CharField(max_length=6, validators=[MinLengthValidator(6), MaxLengthValidator(6)])


class LoginSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(region='UZ')
    password = serializers.CharField()

