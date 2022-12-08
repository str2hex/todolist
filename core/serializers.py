from abc import ABC

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

USER_MODEL = get_user_model()


class CreateUserSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        model = USER_MODEL
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password_repeat']

    def validate(self, attrs):
        password = attrs.get('password')
        password_repeat = attrs.pop('password_repeat')

        try:
            validate_password(password)
        except Exception as e:
            raise serializers.ValidationError(e.messages)

        if password != password_repeat:
            raise serializers.ValidationError("Введеные пароли не совпадают")

        return attrs

    def create(self, validated_data):
        password = validated_data.get('password')
        validated_data['password'] = make_password(password)
        instance = super().create(validated_data)
        return instance


class LoginUserSerializers(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def create(self, validated_data):
        user = authenticate(
            username=validated_data['username'],
            password=validated_data['password'],
        )

        if not user:
            raise AuthenticationFailed
        return user

    class Meta:
        model = USER_MODEL
        fields = ["id", "username", "first_name", "last_name", "email", "password"]


class ProfilesSerializers(serializers.ModelSerializer):
    class Meta:
        model = USER_MODEL
        fields = ['username', 'first_name', 'last_name', 'email']


class UpdatePasswordUserSerializers(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        user = attrs['user']
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError("Введен некорректный пароль")

        try:
            validate_password(attrs['new_password'])
        except Exception as e:
            raise serializers.ValidationError(e.messages)

        return attrs

    def update(self, instance, validated_data):
        instance.password = make_password(validated_data['new_password'])
        instance.save()
        return instance


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField(max_length=100)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
