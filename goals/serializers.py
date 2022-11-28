from rest_framework import serializers

from . import models


class GoalCategorySerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.GoalCategory
        read_only_fields = ("id", "created", "updated", "user")
        fields = '__all__'
