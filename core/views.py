from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from core.serializers import CreateUserSerializers

USER_MODEL = get_user_model()


class CreateUserApiView(CreateAPIView):
    queryset = USER_MODEL
    serializer_class = CreateUserSerializers
