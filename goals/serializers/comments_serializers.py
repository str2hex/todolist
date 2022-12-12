from rest_framework import serializers

from core.serializers import UserSerializer
from goals.models.goalscommets import GoalComment


class CommentsCreateSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalComment
        fields = '__all__'
        read_only_fields = ['created', 'updated', 'user']

    def create(self, validated_data):
        instance = GoalComment.objects.create(**validated_data)
        return instance


class CommentsRUDSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.ModelSerializer())

    class Meta:
        model = GoalComment
        fields = '__all__'
        read_only_fields = ['user']

    def update(self, instance, validated_data):
        instance.text = validated_data.get("text")
        instance.save()
        return instance


class GoalCommentsListSerializers(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = GoalComment
        fields = "__all__"
        read_only_fields = ['created', 'updated', 'user']

