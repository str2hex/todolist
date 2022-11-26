from django.contrib.auth import get_user_model, login
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response

from core.serializers import CreateUserSerializers, LoginUserSerializers

USER_MODEL = get_user_model()


class CreateUserApiView(CreateAPIView):
    queryset = USER_MODEL
    serializer_class = CreateUserSerializers


class LoginUserView(GenericAPIView):
    serializer_class = LoginUserSerializers

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request=request, user=user)
        return Response(serializer.data)