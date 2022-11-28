from rest_framework import serializers

from . import models


class GoalCategorySerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.GoalCategory
        read_only_fields = ("id", "created", "updated", "user")
        fields = '__all__'


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)


class GoalCategorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = models.GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")