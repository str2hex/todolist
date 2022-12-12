from rest_framework import serializers

from core.serializers import UserSerializer
from ..models.board import BoardParticipant
from ..models.goalcategory import GoalCategory


class GoalCategorySerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user")
        fields = '__all__'

    def validate(self, attrs):
        roll = BoardParticipant.objects.filter(
            user=attrs.get('user'),
            board=attrs.get('board'),
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
        ).exists()
        if roll:
            return attrs
        raise serializers.ValidationError('You do not have permission to perform this action')


class GoalCategorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")

    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError('not allowed in deleted category')
        if value.user != self.context['request'].user:
            raise serializers.ValidationError('not owner of category')

        return value