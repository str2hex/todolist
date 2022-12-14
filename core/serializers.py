from abc import ABC

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.validators import UniqueValidator

USER_MODEL = get_user_model()


class CreateUserSerializers(serializers.ModelSerializer):
    """Serializers создания пользователя"""
    password = serializers.CharField(write_only=True)
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        model = USER_MODEL
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'password_repeat']

    def validate(self, attrs) -> dict:
        """Валидация паролей"""
        password = attrs.get('password')
        password_repeat = attrs.pop('password_repeat')

        try:
            validate_password(password)
        except Exception as e:
            raise serializers.ValidationError(e.messages)

        if password != password_repeat:
            raise serializers.ValidationError("Введеные пароли не совпадают")

        return attrs

    def create(self, validated_data: dict) -> USER_MODEL:
        """После успешной валидации создаём пользователя"""
        password = validated_data.get('password')
        validated_data['password'] = make_password(password)
        instance = super().create(validated_data)
        return instance


class LoginUserSerializers(serializers.ModelSerializer):
    """Serializers входа пользователя на аккаунт - login"""
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def create(self, validated_data: dict) -> USER_MODEL:
        """Вход пользователя проверка аутентификации """
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
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class UpdatePasswordUserSerializers(serializers.Serializer):
    """Serializers смены пароля пользователя"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs) -> dict:
        """Валидация пароля пользователя"""
        password_old = attrs.get('old_password')

        user: USER_MODEL = self.instance
        if not user.check_password(password_old):
            raise ValidationError({'old_password': 'is incorrect'})

        try:
            validate_password(attrs['new_password'])
        except Exception as e:
            raise serializers.ValidationError(e.messages)

        return attrs

    def update(self, instance: USER_MODEL, validated_data: dict) -> USER_MODEL:
        """Обновление пароля в БД"""
        instance.set_password(validated_data['new_password'])
        instance.save(update_fields=['password'])
        return instance


class UserSerializer(serializers.Serializer):
    """Стандартный набор пользователя"""
    id = serializers.IntegerField()
    username = serializers.CharField(max_length=100)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()


class RetrieveUserSerializer(serializers.ModelSerializer):
    """Обновление данных пользователя"""
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=USER_MODEL.objects.all())
        ]
    )

    class Meta:
        model = USER_MODEL
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email'
        )
