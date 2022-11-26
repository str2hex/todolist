from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

USER_MODEL = get_user_model()


class CreateUserSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        model = USER_MODEL
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password_repeat']

    def create(self, validated_data):
        password = validated_data.get('password')
        password_repeat = validated_data.pop('password_repeat')
        if password != password_repeat:
            return serializers.ValidationError("Введенные пароли не совпадают")
        validated_data['password'] = make_password(password)
        return super().create(validated_data)


