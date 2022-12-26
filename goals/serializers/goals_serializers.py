import datetime
from rest_framework.serializers import ValidationError
from rest_framework import serializers

from core.serializers import UserSerializer
from goals.models import GoalCategory
from goals.models.goals import Goals


class GoalListSerializers(serializers.ModelSerializer):
    """Вывод списка целей пользователя"""
    user = UserSerializer(read_only=True)

    class Meta:
        model = Goals
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"

    def validate(self, attrs: dict) -> None:
        """Валидация пользователя"""
        if attrs['user'] != self.context['request'].user:
            raise serializers.ValidationError('not owner of category')


class GoalCreateSerializer(serializers.ModelSerializer):
    """Создание цели пользователя"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goals
        fields = "__all__"
        read_only_fields = ["id", "created", "updated", "user"]

    def validate(self, attrs: dict) -> dict:
        """Валидация даты"""
        date = datetime.datetime.today().date()
        if attrs['due_date'] < date:
            raise ValidationError("Дата не может быть в прошлом времени")

        return attrs

    def validate_category(self, value: GoalCategory) -> GoalCategory:
        """Валидация категорий пользователя"""
        if value.is_deleted:
            raise serializers.ValidationError("not allowed in deleted category")
        if value.user != self.context["request"].user:
            raise serializers.ValidationError("not owner of category")
        return value


class GoalsRUDSerializers(serializers.ModelSerializer):
    """Обновление цели пользователя"""
    user = UserSerializer(read_only=True)

    class Meta:
        model = Goals
        fields = "__all__"
        read_only_fields = ["id", "created", "user"]
