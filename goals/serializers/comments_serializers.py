from rest_framework import serializers

from core.serializers import UserSerializer
from goals.models.board import BoardParticipant
from goals.models.goalscommets import GoalComment


class CommentsCreateSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalComment
        read_only_fields = ('id', 'user', 'created', 'updated', 'goal')
        fields = '__all__'

    def validate(self, attrs):
        roll = BoardParticipant.objects.filter(
            user=attrs.get('user'),
            # board=attrs.get('board'),
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
        ).exists()
        if roll:
            return attrs
        raise serializers.ValidationError('You do not have permission to perform this action')

    def create(self, validated_data):
        instance = GoalComment.objects.create(**validated_data)
        return instance


class CommentsRUDSerializers(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = GoalComment
        fields = '__all__'
        read_only_fields = ['user']


class GoalCommentsListSerializers(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = GoalComment
        fields = "__all__"
        read_only_fields = ['created', 'updated', 'user']
