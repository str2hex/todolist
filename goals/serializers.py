from rest_framework import serializers

from . import models


class GoalCategorySerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.GoalCategory
        read_only_fields = ("id", "created", "updated", "user")
        fields = '__all__'


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField(max_length=100)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()


class GoalCategorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = models.GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")