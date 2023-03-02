from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser.conf import settings
from djoser.serializers import UserSerializer, UserCreateSerializer

AuthUser = get_user_model()


class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class RegisterSerializer(UserCreateSerializer):
    class Meta:
        model = AuthUser
        fields = (
            'first_name',
            'last_name',
            'username',
            "password",
        )


class ProfileSerializer(UserSerializer):
    class Meta:
        model = AuthUser
        fields = tuple(AuthUser.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
            'phone_number',
            'address_1',
            'address_2',
            'city',
            'state',
            'zip_code',
        )
        read_only_fields = (settings.LOGIN_FIELD,)


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = AuthUser
        fields = tuple(AuthUser.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
            'phone_number',
            'address_1',
            'address_2',
            'city',
            'state',
            'zip_code',
        )
        read_only_fields = (settings.LOGIN_FIELD,)
