from rest_framework import serializers
from .models import User, Permission


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'street', 'city', 'state', 'zip_code', 'image')
        extra_kwargs = {'email': {'read_only': True}}

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.street = validated_data.get('street', instance.street)
        instance.city = validated_data.get('city', instance.city)
        instance.state = validated_data.get('state', instance.state)
        instance.zip_code = validated_data.get('zip_code', instance.zip_code)
        instance.image = validated_data.get('image', instance.image)

        instance.save()
        return instance


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = ('name', 'description')


class ChangeEmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email',)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.verified = False
        instance.save()

        return instance
