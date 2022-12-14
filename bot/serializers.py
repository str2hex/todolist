from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from bot.models import TgUser


class TgUserSerializer(serializers.ModelSerializer):
    """Верификация пользователя"""
    verification_code = serializers.CharField(write_only=True)

    class Meta:
        model = TgUser
        read_only_fields = ('id', 'tg_chat_id', 'tg_user_id', 'username')
        fields = ('tg_chat_id',
                  'tg_user_id',
                  'username',
                  'verification_code',
                  'user_id')

    def validate(self, attrs: dict) -> dict:
        """Валидация пользователя в телеграмм боте"""
        verification_code = attrs.get('verification_code')
        tg_user = TgUser.objects.filter(
            verification_code=verification_code).first()
        if not tg_user:
            raise ValidationError({'verification_code': 'field is incorrect'})
        attrs['tg_user'] = tg_user
        return attrs
