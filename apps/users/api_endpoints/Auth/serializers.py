from rest_framework import serializers

from django.contrib.auth import get_user_model, authenticate

from phonenumber_field.serializerfields import PhoneNumberField
from phonenumbers import parse, is_valid_number_for_region
from phonenumbers.phonenumberutil import NumberParseException

from apps.book.models import UserStatistics

User = get_user_model()


def validate_phone_number(phone_number):
    try:
        parsed_number = parse(str(phone_number), 'UZ')
        if not is_valid_number_for_region(parsed_number, 'UZ'):
            raise serializers.ValidationError("the phone number should belong only to the region of Uzbekistan")

    except NumberParseException:
        raise serializers.ValidationError("Invalid phone number")


def validate_user(request, data):
    phone_number = data.get('phone_number')
    password = data.get('password')

    user = authenticate(request, phone_number=phone_number, password=password)
    if not user:
        raise serializers.ValidationError("User not found", 404)

    return user


class UserLoginExistsSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(region='UZ', required=True)
    password = serializers.CharField(max_length=64, required=True, write_only=True)

    def validate(self, data):
        validate_phone_number(data.get('phone_number'))

        validate_user(self.context.get('request'), data)

        return data


class UserLoginOtpSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(region='UZ', required=True)
    password = serializers.CharField(max_length=64, required=True, write_only=True)
    code = serializers.CharField(max_length=10, required=True)
    device_id = serializers.CharField(max_length=64, required=True)

    def validate(self, data):
        validate_phone_number(data.get('phone_number'))

        validate_user(self.context.get('request'), data)

        return data


class OtpSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(region='UZ', required=True)
    code = serializers.CharField(max_length=10, required=True)

    def validate(self, data):
        phone_number = data.get('phone_number')
        validate_phone_number(phone_number)
        return data


class UserRegisterExistsSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(region='UZ', required=True)

    def validate(self, data):
        phone_number = data.get('phone_number')

        validate_phone_number(phone_number)

        if User.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError("User already register", 404)

        return data


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone_number', 'full_name', 'age', 'avatar', 'is_premium', 'gender')


class UserStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStatistics
        fields = ('user', 'goals', 'categories')


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'phone_number', 'full_name', 'age', 'avatar', 'is_premium', 'gender', 'password')