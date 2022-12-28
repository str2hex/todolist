import requests as requests
from django.contrib.auth import get_user_model, login, logout
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import serializers

USER_MODEL = get_user_model()


class CreateUserApiView(CreateAPIView):
    """Создание нового пользователя"""
    queryset = USER_MODEL
    serializer_class = serializers.CreateUserSerializers


class LoginUserView(GenericAPIView):
    """Логин пользователя, вход на аккаунт, запись куков"""
    serializer_class = serializers.LoginUserSerializers

    def post(self, request: requests, *args: str, **kwargs: int) -> Response:
        """Получаем от пользователя информацию и сверяем её на валидность"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request=request, user=user)
        return Response(serializer.data)


class ProfileUserView(RetrieveUpdateDestroyAPIView):
    """Вывод информации о пользователе"""
    queryset = USER_MODEL.objects.all()
    serializer_class = serializers.ProfilesSerializers
    permission_classes = [IsAuthenticated]

    def get_object(self) -> USER_MODEL:
        """Определяем pk = user.id"""
        return self.request.user

    def delete(self, request: requests, *args: str, **kwargs: int) -> Response:
        """Выход юзера с аккаунта"""
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdatePasswordUserView(UpdateAPIView):
    queryset = USER_MODEL.objects.all()
    serializer_class = serializers.UpdatePasswordUserSerializers

    def get_object(self) -> USER_MODEL:
        """Определяем pk = user.id"""
        return self.request.user
