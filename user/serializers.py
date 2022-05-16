from django.core.validators import RegexValidator
from rest_framework import serializers
from user.utils import pattern

from user.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number', 'firstname', 'lastname', 'avatar']
        read_only_fields = ('phone_number',)


class UserRegisterSerializer(serializers.ModelSerializer):
    code_regex = RegexValidator(
        regex=r'^\d{6}$', message="123456 holatda kiriting")
    code = serializers.CharField(max_length=6, validators=[code_regex])
    phone_regex = RegexValidator(
        regex=pattern, message="998901234567 holatda kiriting")
    phone_number = serializers.CharField(
        required=True, validators=[phone_regex])

    class Meta:
        model = User
        fields = ['id', 'phone_number', 'firstname',
                  'lastname', 'code', 'password']
        read_only_fields = ('id', )
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5,
                'style': {
                    'input_type': 'password'
                }
            }
        }


class UserCodeSendSerializer(serializers.Serializer):
    phone_regex = RegexValidator(
        regex=pattern, message="998901234567 holatda kiriting")
    phone_number = serializers.CharField(
        required=True, validators=[phone_regex])


class UserLoginSerializer(serializers.Serializer):
    phone_regex = RegexValidator(
        regex=pattern, message="998901234567 holatda kiriting")
    phone_number = serializers.CharField(
        required=True, validators=[phone_regex])
    password = serializers.CharField(required=True)
