from django.contrib.auth import get_user_model, login, logout
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import serializers

USER_MODEL = get_user_model()


class CreateUserApiView(CreateAPIView):
    queryset = USER_MODEL
    serializer_class = serializers.CreateUserSerializers


class LoginUserView(GenericAPIView):
    serializer_class = serializers.LoginUserSerializers

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request=request, user=user)
        return Response(serializer.data)


class ProfileUserView(RetrieveUpdateDestroyAPIView):
    queryset = USER_MODEL.object.all()
    serializer_class = serializers.ProfilesSerializers
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

